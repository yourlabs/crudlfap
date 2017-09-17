#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "crudlfap_example.settings"
    )
    from django.core.management import call_command, execute_from_command_line
    if sys.argv[1] == 'runserver':
        import django
        django.setup()
        call_command('migrate')

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
