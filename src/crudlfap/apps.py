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

    def get_default_views(self):  # pylint: disable=no-self-use
        """Return the default views to use in a new router."""
        crudlfap = getattr(settings, 'CRUDFLAP', {})
        views = crudlfap.get(
            'default_views',
            [
                'crudlfap.views.generic.CreateView',
                'crudlfap.views.generic.DeleteView',
                'crudlfap.views.generic.UpdateView',
                'crudlfap.views.generic.DetailView',
                'crudlfap.views.generic.ListView',
            ]
        )

        return views
