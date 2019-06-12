.. image:: https://img.shields.io/readthedocs/crudlfap.svg
   :target: https://crudlfap.readthedocs.io
.. image:: https://yourlabs.io/oss/crudlfap/badges/master/build.svg
   :target: https://circleci.com/gh/yourlabs/crudlfap
.. image:: https://img.shields.io/codecov/c/github/yourlabs/crudlfap/master.svg
   :target: https://codecov.io/gh/yourlabs/crudlfap
.. image:: https://img.shields.io/npm/v/crudlfap.svg
   :target: https://www.npmjs.com/package/crudlfap
.. image:: https://img.shields.io/pypi/v/crudlfap.svg
   :target: https://pypi.python.org/pypi/crudlfap

Welcome to CRUDLFA+ for Django 2.0: because Django is FUN !
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CRUDLFA+ stands for Create Read Update Delete List Form Autocomplete and more.

This plugin for Django makes a rich user interface from Django models.

Try
===

This should start the example project from ``src/crudlfap_example`` where each
documented example lives, without virtualenv::

    # This installs the repo in ./src/crudlfap and in your python user packages, i run this from ~
    pip install --user -e git+https://github.com/yourlabs/crudlfap.git#egg=crudlfap[dev]

    # Migrate SQLite database, create some users and starts a server on localhost:8000
    crudlfap dev

    # Start webpack watcher
    yarn --cwd js start

Features
========

- DRY into ModelRouter for all views of a Model,
- Rich frontend interface out of the box, MaterializeCSS/Turbolinks/StimulusJS/Webpack

Resources
=========

- `Presentation graciously served by
  <https://gitpitch.com/yourlabs/crudlfap/master>`_ by `GitPitch
  <https://gitpitch.com>`_
- `ChatRoom graciously hosted by
  <https://www.yourlabs.chat>`_ by `YourLabs Business Service
  <https://www.yourlabs.biz>`_ on `Mattermost
  <https://mattermost.com/>`_
- `**Documentation** graciously hosted
  <http://crudlfap.readthedocs.io>`_ by `RTFD
  <http://rtfd.org>`_
- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- For **Security** issues, please contact yourlabs-security@googlegroups.com
- `Git graciously hosted
  <https://yourlabs.io/oss/crudlfap/>`_ by `YourLabs Business Service
  <https://www.yourlabs.biz>`_ with `GitLab
  <https://www.gitlab.org>`_
- `Package graciously hosted
  <http://pypi.python.org/pypi/crudlfap/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Continuous integration graciously hosted
  <https://yourlabs.io/oss/crudlfap/pipelines>`_ by YourLabs Business Service
- Browser test graciously hosted by `SauceLabs
  <https://saucelabs.com>`_
- `**Online paid support** provided via HackHands
  <https://hackhands.com/jpic/>`_,
