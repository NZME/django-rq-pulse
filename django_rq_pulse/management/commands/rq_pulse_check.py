# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import time
from rq import Queue, Worker
from redis import Redis
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Check that the rq workers are processing queued jobs.
    
    If the number of reported rqworkers from redis is not expected or
    If the queue has items but its size does not change over time 
    then it is likely that the workers are down so we notify admins.
    """

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument('--expected-num-workers', dest='expected_num_workers', type=int, default=2, 
                            help='The expected number of running workers.')
        parser.add_argument('--seconds-to-sleep', dest='seconds_to_sleep', type=int, default=5, 
                            help='The number of seconds to sleep before checking the queue size.')
        parser.add_argument('--num-retries', dest='num_retries', type=int, default=5, 
                            help='The number of times we check the queue size before deciding whether it is changing.')
        parser.add_argument('--queue-name', dest='queue_name', default='default', 
                            help='The name of the queue to check.')
    
    def handle(self, *args, **options):
        """Handle command logic."""
        log.info('Checking rq workers')

        self.expected_num_workers = options['expected_num_workers']
        self.seconds_to_sleep = options['seconds_to_sleep']
        self.num_retries = options['num_retries']
        self.queue_name = options['queue_name']
        
        redis_conn = Redis()

        # Check the number of workers is as expected and notify otherwise
        workers = Worker.all(connection=redis_conn)
        num_workers = len(workers)

        if num_workers != self.expected_num_workers:
            subject = 'WARNING: RQ Workers maybe down!'
            message = 'The number of workers {} does not equal the expected number {}. Workers maybe down.'.format(
                num_workers, self.expected_num_workers)
            self.notify(subject, message)

        # Check the Queue size is changing and notify otherwise
        self.q = Queue(self.queue_name, connection=redis_conn)
        self.q_size = len(self.q)

        if self.q_size > 0:
            log.info('The Q has items')
            for i in range(self.num_retries):
                is_q_size_changing = self.sleep_and_check()
                if is_q_size_changing:
                    log.info('The Q size is changing, this is good.')
                    break
                else:
                    log.info('The Q size is not changing, will check again after {} seconds.'.format(self.seconds_to_sleep))
            
            if not is_q_size_changing:
                subject = 'WARNING: RQ Workers maybe down!'
                message = 'The Q size is not changing, this is bad. Workers maybe down.'
                self.notify(subject, message)

        log.info('Finished checking rq workers')

    def notify(self, subject, message):
        """Given a subject and a message, send an email to ADMINS."""
        log.info(subject)
        log.info(message)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, settings.ADMINS)

    def sleep_and_check(self):
        """Sleep for a number of seconds then check if the queue size has changed."""
        time.sleep(self.seconds_to_sleep)
        return self.q_size != len(self.q)
