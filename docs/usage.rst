=====
Usage
=====

To use Django RQ Pulse in a project, add it to your `INSTALLED_APPS`:

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
