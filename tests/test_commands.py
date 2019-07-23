#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.core.management import call_command
from django.test import TestCase
from django.conf import settings
import mock
from django_rq_pulse.management.commands import rq_pulse_check


@mock.patch.object(rq_pulse_check, 'time')
@mock.patch.object(rq_pulse_check, 'log')
@mock.patch.object(rq_pulse_check, 'mail_admins')
@mock.patch.object(rq_pulse_check, 'Worker')
@mock.patch.object(rq_pulse_check, 'Queue')
@mock.patch.object(rq_pulse_check, 'Redis', mock.MagicMock())
class RQPulseCheckTestCase(TestCase):
    def test_number_of_workers_is_not_expected(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_worker.all.return_value = []
        call_command('rq_pulse_check')
        mock_mail_admins.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 0 does not equal the expected number 2. Workers maybe down.')

        mock_worker.all.return_value = [mock.MagicMock()]
        call_command('rq_pulse_check')
        mock_mail_admins.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 1 does not equal the expected number 2. Workers maybe down.')

    def test_number_of_workers_is_expected(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_worker.all.return_value = [mock.MagicMock(), mock.MagicMock()]
        call_command('rq_pulse_check')
        self.assertFalse(mock_mail_admins.called)

    def test_minimum_number_of_workers_is_not_expected(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_worker.all.return_value = []
        call_command('rq_pulse_check', minimum_num_workers=2)
        mock_mail_admins.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 0 is less than the expected number 2. Workers may be down.')

        mock_worker.all.return_value = [mock.MagicMock()]
        call_command('rq_pulse_check', minimum_num_workers=2)
        mock_mail_admins.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 1 is less than the expected number 2. Workers may be down.')

    def test_minimum_number_of_workers_is_expected(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_worker.all.return_value = [mock.MagicMock(), mock.MagicMock()]
        call_command('rq_pulse_check')
        self.assertFalse(mock_mail_admins.called)

    def test_queue_has_no_items(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_queue.return_value.__len__.return_value = 0
        call_command('rq_pulse_check', minimum_num_workers=2)
        self.assertFalse(mock_time.sleep.called)

    def test_queue_has_items_and_queue_size_not_changing(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_worker.all.return_value = [mock.MagicMock(), mock.MagicMock()]
        mock_queue.return_value.__len__.return_value = 1
        call_command('rq_pulse_check')
        self.assertListEqual(mock_time.sleep.call_args_list, 
                             [mock.call(5), mock.call(5), mock.call(5), mock.call(5), mock.call(5)])
        mock_mail_admins.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The Q size is not changing, this is bad. Workers maybe down.')

    def test_queue_has_items_and_queue_size_is_changing(
        self, mock_queue, mock_worker, mock_mail_admins, mock_log, mock_time):
        mock_worker.all.return_value = [mock.MagicMock(), mock.MagicMock()]
        mock_queue.return_value.__len__.side_effect = [10, 9]
        call_command('rq_pulse_check')
        self.assertListEqual(mock_time.sleep.call_args_list, [mock.call(5)])
        self.assertFalse(mock_mail_admins.called)