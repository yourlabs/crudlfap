"""Django AppConfig for the crudlfap module."""

from django import apps

from . import views


class DefaultConfig(apps.AppConfig):
    """Default AppConfig."""

    name = 'crudlfap'

    def get_default_views(self):  # pylint: disable=no-self-use
        """Return the default views to use in a new router."""
        return [
            views.CreateView,
            views.DeleteView,
            views.DetailView,
            views.ListView,
            views.UpdateView,
        ]
