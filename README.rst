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

```python
INSTALLED_APPS = (
    ...
    'django_rq_pulse.apps.DjangoRqPulseConfig',
    ...
)
```

Usage
--------

```python
# Check that rqworkers are running.
# If the actual number of workers is not equal the expected number of workers or
# If there are items in the queue but the queue size is not changing notify admins by email.
python manage.py rq_pulse_check

# The above command will run with default parameters where
# --expected-num-workers=2
# --seconds-to-sleep=5
# --num-retries=5
# --queue-name="default"

# You can override these values by passing any or all the parameters to the command like so:
python manage.py rq_pulse_check --expected-num-workers=3 --queue-name="high"

# To get a list of the command parameters use the --help parameter.
python manage.py rq_pulse_check --help
```
    
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
