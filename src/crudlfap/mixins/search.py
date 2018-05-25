from betterforms.changelist import SearchForm


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

    def get_search_form(self, queryset=None):
        if self.search_fields:
            form = self.search_form_class(
                self.request.GET,
                queryset=queryset or self.object_list
            )
            form.full_clean()
            return form
