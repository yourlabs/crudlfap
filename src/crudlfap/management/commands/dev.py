from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Migrate/Createsuperuser/Runserver'

    def handle(self, *args, **options):
        call_command('migrate')

        from django.conf import settings
        from django.apps import apps
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        if not user_model.objects.count():
            call_command('createsuperuser')

        call_command('runserver')
