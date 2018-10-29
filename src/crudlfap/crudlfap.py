# flake8: noqa: F401
"""Import everything we expose in crudlfap namespace."""

from .apps import _installed
from .factory import Factory
from .mixins import *  # noqa
from .registry import Registry
from .route import Route
from .router import Router, Views, ViewsDescriptor
from .site import site
from .views import *  # noqa
