CRUDLFA+ Tutorial
~~~~~~~~~~~~~~~~~

About document
--------------

This document attempts to teach the patterns you can use, and at the same time
go through every feature. The document strives to teach CRUDLFA+ as efficiently
as possible. If it becomes too long, we will see how we refactor the document,
until then, it serves as main documentation. Please contribute any modification
you feel this document needs to fit its purpose.

About module
------------

CRUDLFA+ strives to provide a modern UI for Django generic views out of the
box, but all defaults should also be overiddable as conveniently as possible.
It turns out that Django performs extremely well already, but by pushing
Django's philosophy such as DRY as far as possible, even in the client side
code world.

Settings
--------

You can consult the settings for your crudlfap version in
the :py:module:`~crudlfap_example.settings` module. We're
going to setup ``TEMPLATES`` and ``INSTALLED_APPS``.

TEMPLATES
`````````

CRUDLFA+ requires jinja2 templates is Jinja2, you can
either integrate reference settings in your own template
backend configuration. If you don't have any, just
importing the backend configuration should work, add to
settings.py:

.. code-block:: python

    from crudlfap.settings import TEMPLATES

.. note:: Alternatively, you could import

INSTALLED_APPS
``````````````


