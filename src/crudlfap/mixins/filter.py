from django.db import models

import django_filters


class FilterMixin(object):
    def get_filterset(self):
        """
        Returns an instance of the filterset to be used in this view.
        """
        fs = self.filterset_class(**self.filterset_kwargs)

        # filter out choices which have no result to avoid filter pollution
        # with choices which would empty out results
        for name, field in fs.form.fields.items():
            try:
                mf = self.model._meta.get_field(name)
            except:
                continue

            if not isinstance(mf, models.ForeignKey):
                continue

            field.queryset = field.queryset.annotate(
                c=models.Count(mf.related_query_name())
            ).filter(c__gt=0)

        return fs

    def get_filterset_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {
            'data': self.request.GET or None,
            'request': self.request,
            'queryset': self.queryset,
        }

    def get_filterset_meta_filter_overrides(self):
        return {
            models.CharField: {
               'filterset_class': django_filters.CharFilter,
               'extra': lambda f: {
                   'lookup_expr': 'icontains',
               },
            },
        }

    def get_filter_fields(self):
        return []

    def get_filterset_meta_attributes(self):
        return dict(
            model=self.model,
            fields=self.filter_fields,
            filter_overrides=self.filterset_meta_filter_overrides
        )

    def get_filterset_meta_class(self):
        return type('Meta', (object,), self.filterset_meta_attributes)

    def get_filterset_class_attributes(self):
        return dict(Meta=self.filterset_meta_class)

    def get_filterset_class(self):
        return type(
            '{}FilterSet'.format(self.model.__name__),
            (django_filters.FilterSet,),
            self.filterset_class_attributes
        )
