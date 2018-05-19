CRUDLFA+ Tutorial
~~~~~~~~~~~~~~~~~

About document
==============

This document attempts to teach the patterns you can use, and at the same time
go through every feature. The document strives to teach CRUDLFA+ as efficiently
as possible. If it becomes too long, we will see how we refactor the document,
until then, it serves as main documentation. Please contribute any modification
you feel this document needs to fit its purpose.

About module
============

CRUDLFA+ strives to provide a modern UI for Django generic views out of the
box, but all defaults should also be overiddable as conveniently as possible.
It turns out that Django performs extremely well already, but by pushing
Django's philosophy such as DRY as far as possible, even in the client side
code world.

Enable in your project
======================

We're going to setup ``TEMPLATES`` and ``INSTALLED_APPS`` before we begin.

.. note:: We will review the minimal settings in this tutorial, but you can
          consult the default settings available for your crudlfap version in
          the :py:mod:`~crudlfap.settings` module.

TEMPLATES
---------

CRUDLFA+ uses Jinja2 templates with a quite extended configuration. Options to
enable them are using any of these in your settings:

- easiest: :py:data:`crudlfap.settings.TEMPLATES`
- intermediate: :py:data:`crudlfap.settings.CRUDLFAP_TEMPLATE_BACKEND`
- custom: :py:data:`crudlfap.settings.DEFAULT_TEMPLATE_BACKEND`

INSTALLED_APPS
--------------

CRUDLFA+ leverages apps from the Django ecosystem.
Use :py:data:`crudlfap.settings.CRUDLFAP_TEMPLATE_BACKEND`. To help make this a
pleasant experience, CRUDLFAP+ splits the INSTALLED_APPS setting into multiple
settings you can import and mix together:

- everything: :py:data:`crudlfap.settings.INSTALLED_APPS`,
- crudlfap only: :py:data:`crudlfap.settings.CRUDLFAP_APPS`,
- django apps: :py:data:`crudlfap.settings.DJANGO_APPS`,

Define a Router
===============

Register a CRUD with default views using Router.register()
----------------------------------------------------------

Just add a ``crudlfap.py`` file in one of your installed apps, and the
:py:class:`~crudlfap.apps.DefaultConfig` will autodiscover them, this example
shows how to enable the default CRUD for a custom model:

.. literalinclude:: ../src/crudlfap_example/artist/crudlfap.py

In this case, the :py:class:`~crudlfap.router.Router` will get the views
it should serve from the :py:data:`~crudlfap.settings.CRUDLFAP_VIEWS`
setting.

Custom view parameters with View.clone()
----------------------------------------

If you want to specify views in the router::

.. literalinclude:: ../src/crudlfap_example/song/crudlfap.py

Using the :py:meth:`~crudlfap.factory.Factory.clone()` classmethod will
define a subclass on the fly with the given attributes.



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
