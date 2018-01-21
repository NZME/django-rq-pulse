=============================
Django RQ Pulse
=============================

.. image:: https://badge.fury.io/py/django-rq-pulse.svg
    :target: https://badge.fury.io/py/django-rq-pulse

.. image:: https://travis-ci.org/NZME/django-rq-pulse.svg?branch=master
    :target: https://travis-ci.org/NZME/django-rq-pulse

A Django package to check that rq workers are running and notify admins if they are not

Quickstart
----------

Install Django RQ Pulse::

    pip install django-rq-pulse

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_rq_pulse.apps.DjangoRqPulseConfig',
        ...
    )

Add Django RQ Pulse's URL patterns:

.. code-block:: python

    from django_rq_pulse import urls as django_rq_pulse_urls


    urlpatterns = [
        ...
        url(r'^', include(django_rq_pulse_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
