"""Import everything we expose in crudlfap namespace."""

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
