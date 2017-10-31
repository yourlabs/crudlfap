"""Import everything we expose in crudlfap namespace."""

from django.utils.module_loading import import_string

from .apps import _installed
from .routers import Router
from .views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    ModelViewMixin,
    ObjectFormView,
    ObjectViewMixin,
    UpdateView,
    View,
    ViewMixin,
)

if _installed('crudlfap_filtertables2'):
    from crudlfap_filtertables2.views import FilterTables2ListView
