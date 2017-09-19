"""Django AppConfig for the crudlfap module."""

from django import apps
from django.conf import settings

from .views import generic


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
        views = [
            'crudlfap.views.generic.DeleteView',
            'crudlfap.views.generic.UpdateView',
            'crudlfap.views.generic.DetailView',
            'crudlfap.views.generic.CreateView',
        ]

        if _installed('crudlfap_filtertables2'):
            from crudlfap_filtertables2.views import FilterTables2ListView
            views.append(FilterTables2ListView)
        else:
            views.append(generic.ListView)

        return views
