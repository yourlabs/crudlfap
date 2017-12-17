"""
Base manage.main hack which supports being an entry point.

In your project setup.py, add::

    entry_points={
        'console_scripts': [
            'yourproject = yourproject.manage:main',
        ],
    }

Then, setup your manage.py as such::

    #!/usr/bin/env python
    import os
    from crudlfap.manage import main

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

    if __name__ == '__main__':
        main()

Note that it will enable DEBUG env var, which wsgi.py should **not** enable. By
doing so, this prevents any server using the entry point from having DEBUG
enabled by default and any developer from not having DEBUG enabled by default.
"""
import os
import sys
import warnings


def main():
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
