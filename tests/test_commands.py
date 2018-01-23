#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.test import TestCase
import mock
from django.conf import settings
from django_rq_pulse.management.commands import rq_pulse_check

@mock.patch.object(rq_pulse_check, 'time')
@mock.patch.object(rq_pulse_check, 'log')
@mock.patch.object(rq_pulse_check, 'send_mail')
@mock.patch.object(rq_pulse_check, 'Worker')
@mock.patch.object(rq_pulse_check, 'Queue')
@mock.patch.object(rq_pulse_check, 'Redis', mock.MagicMock())
@mock.patch.object(settings, 'DEFAULT_FROM_EMAIL', 'sample_from@email.com')
@mock.patch.object(settings, 'ADMINS', ['sample_admin@email.com'])
class RQPulseCheckTestCase(TestCase):
    def test_number_of_workers_is_not_expected(self, mock_queue, mock_worker, mock_send_mail,
                                               mock_log, mock_time):
        mock_worker.all.return_value = []
        call_command('rq_pulse_check')
        mock_send_mail.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 0 does not equal the expected number 2. Workers maybe down.', 
            'sample_from@email.com', ['sample_admin@email.com'])

        mock_worker.all.return_value = [mock.MagicMock()]
        call_command('rq_pulse_check')
        mock_send_mail.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 1 does not equal the expected number 2. Workers maybe down.', 
            'sample_from@email.com', ['sample_admin@email.com'])

    def test_number_of_workers_is_expected(self, mock_queue, mock_worker, mock_send_mail,
                                           mock_log, mock_time):
        mock_worker.all.return_value = [mock.MagicMock(), mock.MagicMock()]
        call_command('rq_pulse_check')
        self.assertFalse(mock_send_mail.called)

    def test_queue_has_no_items(self, mock_queue, mock_worker, mock_send_mail,
                             mock_log, mock_time):
        mock_queue.return_value.__len__.return_value = 0
        call_command('rq_pulse_check')
        self.assertFalse(mock_time.sleep.called)

    def test_queue_has_items(self, mock_queue, mock_worker, mock_send_mail,
                             mock_log, mock_time):
        mock_queue.return_value.__len__.return_value = 1
        call_command('rq_pulse_check')
        self.assertListEqual(mock_time.sleep.call_args_list, 
                             [mock.call(5), mock.call(5), mock.call(5), mock.call(5), mock.call(5)])
        