#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.test import TestCase
import mock
from django.conf import settings
from django_rq_pulse.management.commands import rq_pulse_check

@mock.patch.object(rq_pulse_check, 'send_mail')
@mock.patch.object(settings, 'DEFAULT_FROM_EMAIL', 'sample_from@email.com')
@mock.patch.object(settings, 'ADMINS', ['sample_admin@email.com'])
class RQPulseCheckTestCase(TestCase):
    def test_number_of_workers_is_not_expected(self, mock_send_mail):
        call_command('rq_pulse_check')
        mock_send_mail.assert_called_with(
            'WARNING: RQ Workers maybe down!', 
            'The number of workers 0 does not equal the expected number 2. Workers maybe down.', 
            'sample_from@email.com', ['sample_admin@email.com'])
