"""
Base manage.main hack which supports being an entry point.

In your project setup.py, add::

    entry_points={
        'console_scripts': [
            'yourproject = yourproject.manage:main',
        ],
    }

Replace your manage.py content with::

    #!/usr/bin/env python
    from crudlfap.manage import main

    if __name__ == '__main__':
        main('yourproject.settings')

Note that it will enable DEBUG env var, which wsgi.py should **not** enable.
"""
import os
import sys
import warnings


def main(settings_module=None):
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        settings_module or 'crudlfap_example.settings'
    )

    if 'DEBUG' not in os.environ:
        warnings.warn('DEFAULTING DEBUG=1')
        os.environ.setdefault('DEBUG', '1')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Couldn\'t import Django. Are you sure it\'s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)
