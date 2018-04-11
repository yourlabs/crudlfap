Install CRUDLFA+ in your project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Settings
========

The easy way, in settings.py::

    from crudlfap.settings import CRUDLFAP_APPS, TEMPLATES
    INSTALLED_APPS += CRUDLFAP_APPS


If you already have a TEMPLATES settings, import CRUDLFAP_TEMPLATE_BACKEND
instead of TEMPLATES::

    TEMPLATES = [
        CRUDLFAP_TEMPLATE_BACKEND,
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # etc
        }
    ]

URLs
====

The easiest configuration is to generate patterns from the default registry::

    from crudlfap import crudlfap

    urlpatterns = [
        crudlfap.site.urlpattern
    ]

Or, to sit in ``/admin``::

    urlpatterns = [
        crudlfap.site.get_urlpattern('admin'),
        # your patterns ..
    ]

crudlfap.py
===========

CRUDLFA+ autodiscovers ``crudlfap.py`` in every installed app. Here's a simple
example to get started::

    from crudlfap import crudlfap

    from .models import Artist

    crudlfap.Router(Artist).register()
