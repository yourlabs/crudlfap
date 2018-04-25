.. image:: https://img.shields.io/readthedocs/crudlfap.svg?style=for-the-badge
   :target: https://crudlfap.readthedocs.io
.. image:: https://img.shields.io/circleci/project/github/yourlabs/crudlfap/master.svg?style=for-the-badge
   :target: https://circleci.com/gh/yourlabs/crudlfap
.. image:: https://img.shields.io/codecov/c/github/yourlabs/crudlfap/master.svg?style=for-the-badge
   :target: https://codecov.io/gh/yourlabs/crudlfap
.. image:: https://img.shields.io/npm/v/crudlfap.svg?style=for-the-badge
   :target: https://www.npmjs.com/package/crudlfap
.. image:: https://img.shields.io/pypi/v/crudlfap.svg?style=for-the-badge
   :target: https://pypi.python.org/pypi/crudlfap

Welcome to CRUDLFA+ for Django 2.0: because Django is FUN !
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CRUDLFA+ stands for Create Read Update Delete List Form Autocomplete and more.

This plugin for Django makes a rich user interface from Django models.

Try
===

This should start the example project in ``src/crudlfap_example`` where each
documented example lives, without virtualenv::

    # This installs the repo in ./src/crudlfap and in your python user packages, i run this from ~
    pip install --user -e git+https://github.com/yourlabs/crudlfap.git#egg=crudlfap[dev]

    # Migrate SQLite database, create some users and starts a server on localhost:8000
    crudlfap dev

    # Start webpack watcher
    yarn start

Features
========

- DRY into ModelRouter for all views of a Model,
- Rich frontend interface out of the box, MaterializeCSS/Turbolinks/StimulusJS/Webpack

Resources
=========

- `**Documentation** graciously hosted
  <http://crudlfap.readthedocs.io>`_ by `RTFD
  <http://rtfd.org>`_
- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- For **Security** issues, please contact yourlabs-security@googlegroups.com
- `Git graciously hosted
  <https://github.com/yourlabs/crudlfap/>`_ by `GitHub
  <http://github.com>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/crudlfap/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Continuous integration graciously hosted
  <http://circleci.com/gh/yourlabs/crudlfap>`_ by `CircleCI
  <http://circleci.com>`_
- Browser test graciously hosted by `SauceLabs
  <https://saucelabs.com>`_
- `**Online paid support** provided via HackHands
  <https://hackhands.com/jpic/>`_,
