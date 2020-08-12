from functools import reduce
import operator

from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _


class SearchForm(forms.Form):
    q = forms.CharField(label=_('Search'), required=False)


class SearchMixin(object):
    def get_search_fields(self):
        if hasattr(self.router, 'search_fields'):
            return self.router.search_fields
        return [
            f.name
            for f in self.model._meta.fields
            if isinstance(f, models.CharField)
        ]

    def get_search_form_class(self):
        if not self.search_fields:
            return

        return SearchForm

    def get_search_form(self):
        if self.search_fields:
            self.search_form = self.search_form_class(
                self.request.GET,
            )
            self.search_form.full_clean()
        else:
            self.search_form = None
        return self.search_form

    def search_filter(self, qs):
        q = self.search_form.cleaned_data.get('q', '')

        if not self.search_fields or not q:
            return qs

        return qs.filter(reduce(
            operator.or_,
            [
                Q(**{search_field + '__icontains': q})
                for search_field in self.search_fields
            ]
        )).distinct()
