Install CRUDLFA+ module
~~~~~~~~~~~~~~~~~~~~~~~

This section concerns
This package can be installed from PyPi by running:

Installing from PyPi
--------------------

If you are just getting started with CRUDLFA+, it is recommended that you
start by installing the latest version from the Python Package Index (PyPi_).
To install CRUDLFA+ from PyPi using pip run the following command in your terminal.

.. code-block:: bash

   pip install crudlfap

If you are not in a virtualenv_, the above will fail if not executed as root,
in this case use ``install --user``::

    pip install --user crudlfap

With development packages
-------------------------

If you intend to run the ``crudlfap dev`` command, then you should have the
development dependencies by adding ``[dev]``::

    pip install (--user) crudlfap[dev]

Then, you should see the example project running on port 8000 with command::

    crudlfap dev

Installing from GitHub
----------------------

You can install the latest current trunk of crudlfap directly from GitHub using pip_.

.. code-block:: bash

   pip install --user -e git+git://github.com/yourlabs/crudlfap.git@master#egg=crudlfap[dev]

.. warning:: ``[dev]``, ``--user``, ``@master`` are all optionnal above.

Installing from source
----------------------

1. Download a copy of the code from GitHub. You may need to install git_.

.. code-block:: bash

   git clone https://github.com/yourlabs/crudlfap.git

2. Install the code you have just downloaded using pip, assuming your current
   working directory has not changed since the previous command it could be::

       pip install -e ./crudlfap[dev]

Move on to the :doc:`tutorial`.

.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _pip: https://pip.pypa.io/en/stable/installing/
.. _PyPi: https://pypi.python.org/pypi
