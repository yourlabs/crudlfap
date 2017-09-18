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
        from django.conf import settings
        from django.apps import apps
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        if not user_model.objects.count():
            call_command('createsuperuser')

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
