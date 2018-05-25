import collections

from django import forms
from django import template
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.utils.safestring import mark_safe

import django_filters

from .. import mixins
from ..site import site


class BaseListView(mixins.ModelMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'crudlfap/list.html'

    def get(self, *a, **k):
        '''Enforce sane default paginate_by if not False.'''
        if getattr(self, 'paginate_by', None) is None:
            self.paginate_by = self.get_paginate_by()
        return super().get(*a, **k)

    def get_paginate_by(self, queryset=None):
        if self.router and hasattr(self.router, 'paginate_by'):
            return self.router.paginate_by
        return 10
