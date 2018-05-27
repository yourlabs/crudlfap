from betterforms.changelist import SearchForm

from django import forms
from django.db import models
from django.utils.translation import ugettext as _


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

        return type(
            self.model.__name__ + 'SearchForm',
            (SearchForm,),
            dict(
                SEARCH_FIELDS=self.search_fields,
                model=self.model,
                q=forms.CharField(label=_('Search'), required=False)
            )
        )

    def get_search_form(self):
        if self.search_fields:
            self.search_form = self.search_form_class(
                self.request.GET,
                queryset=self.object_list
            )
            self.search_form.full_clean()
        else:
            self.search_form = None
        return self.search_form
