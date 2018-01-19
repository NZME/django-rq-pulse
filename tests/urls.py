# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_rq_pulse.urls import urlpatterns as django_rq_pulse_urls

urlpatterns = [
    url(r'^', include(django_rq_pulse_urls, namespace='django_rq_pulse')),
]
