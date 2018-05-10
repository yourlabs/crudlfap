Install CRUDLFA+ in your project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package can be installed from PyPi by running:

Installing from PyPi
--------------------

If you are just getting started with CRUDLFA+, it is recommended that you
start by installing the latest version from the Python Package Index (`PyPi`_).
To install CRUDLFA+ from PyPi using pip run the following command in your terminal.

.. code-block:: bash

   pip install crudlfap


Installing from GitHub
----------------------

You can install the latest **development** version of crudlfap directly from GitHub using :code:`pip`.

.. code-block:: bash

   pip install -e git+git://github.com/yourlabs/crudlfap.git@master


Installing from source
----------------------

1. Download a copy of the code from GitHub. You may need to install `git`_.

.. code-block:: bash

   git clone https://github.com/yourlabs/crudlfap.git

2. Install the code you have just downloaded using pip

.. code-block:: bash

   pip install -e /path/to/crudlfap[dev]




Settings
========

The easy way, in settings.py::

    from crudlfap.settings import CRUDLFAP_APPS, TEMPLATES
    INSTALLED_APPS += CRUDLFAP_APPS


You also need to remove the ``django.contrib.admin`` from the your existing ``INSTALLED_APPS`` or you can pop this::

    CRUDLFAP_APPS.pop(CRUDLFAP_APPS.index('django.contrib.admin'))


If you already have a ``TEMPLATES`` settings, import ``CRUDLFAP_TEMPLATE_BACKEND``
instead of ``TEMPLATES``::

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



.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _pip: https://pip.pypa.io/en/stable/installing/
.. _PyPi: https://pypi.python.org/pypi