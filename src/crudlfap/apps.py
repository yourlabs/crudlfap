"""Django AppConfig for the crudlfap module."""

from django import apps
from django.conf import settings


def _installed(*apps):
    for app in apps:
        if app not in settings.INSTALLED_APPS:
            return False
    return True


class DefaultConfig(apps.AppConfig):
    """Default AppConfig."""

    name = 'crudlfap'

    def ready(self):
        super().ready()
        self.module.autodiscover()
