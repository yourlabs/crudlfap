"""Import everything we expose in crudlfap namespace."""

from django.utils.module_loading import import_string

from .apps import _installed
from .factory import Factory
from .registry import Registry
from .site import site
from .route import Route
from .router import Router
from .views.debug import UrlsView
from .views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    ModelViewMixin,
    ObjectFormView,
    ObjectView,
    ObjectViewMixin,
    UpdateView,
    View,
    ViewMixin,
)

if _installed('crudlfap_filtertables2'):
    from crudlfap_filtertables2.views import FilterTables2ListView
