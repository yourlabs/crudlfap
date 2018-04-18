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

    def get_default_model_views(self):  # pylint: disable=no-self-use
        """Return the default views to use in a new router."""
        crudlfap = getattr(settings, 'CRUDFLAP', {})

        if _installed('crudlfap_filtertables2'):
            list_view = 'crudlfap_filtertables2.views.FilterTables2ListView'
        else:
            list_view = 'crudlfap.views.generic.ListView'

        views = crudlfap.get(
            'default_views',
            [
                'crudlfap.views.generic.CreateView',
                'crudlfap.views.generic.DeleteView',
                'crudlfap.views.generic.UpdateView',
                'crudlfap.views.generic.DetailView',
                list_view,
            ]
        )

        return views

    def ready(self):
        super().ready()
        self.module.autodiscover()
