import django_filters
from django import forms
from django.db import models


class FilterMixin(object):
    def get_filter_model(self):
        return self.filterset_kwargs['queryset'].model

    def get_filterset(self):
        """
        Returns an instance of the filterset to be used in this view.
        """
        self.filterset = self.filterset_class(**self.filterset_kwargs)

        # filter out choices which have no result to avoid filter pollution
        # with choices which would empty out results
        for name, field in self.filterset.form.fields.items():
            try:
                mf = self.filter_model._meta.get_field(name)
            except Exception:
                continue

            if not isinstance(mf, models.ForeignKey):
                continue

            field.queryset = field.queryset.annotate(
                c=models.Count(mf.related_query_name())
            ).filter(c__gt=0)

    def get_filterset_data(self):
        return self.request.GET.copy()

    def get_filterset_kwargs(self):
        """
        Returns the keyword arguments for instanciating the filterset.
        """
        return {
            'data': self.filterset_data,
            'request': self.request,
            'queryset': self.queryset,
        }

    def get_filterset_meta_filter_overrides(self):
        return {
            models.CharField: {
               'filterset_class': django_filters.CharFilter,  # noqa
               'extra': lambda f: {
                   'lookup_expr': 'icontains',
               },
            },
        }

    def get_filter_fields(self):
        return []

    def get_filterset_form_class(self):
        return type(
            'FiltersetForm',
            (forms.Form,),
            {
                '_layout': self.filterset_form_layout,
            }
        )

    def get_filterset_form_layout(self):
        return None

    def get_filterset_meta_attributes(self):
        return dict(
            model=self.filter_model,
            fields=self.filter_fields,
            filter_overrides=self.filterset_meta_filter_overrides,
            form=self.filterset_form_class,
        )

    def get_filterset_meta_class(self):
        return type('Meta', (object,), self.filterset_meta_attributes)

    def get_filterset_extra_class_attributes(self):
        extra = dict()
        for field_name in self.filter_fields:
            try:
                field = self.filter_model._meta.get_field(field_name)
            except:  # noqa
                continue
            choices = getattr(field, 'choices', None)
            if choices is None:
                continue
            extra[field_name] = django_filters.MultipleChoiceFilter(
                choices=choices)
        return extra

    def get_filterset_class_attributes(self):
        res = dict(Meta=self.filterset_meta_class)
        res.update(self.filterset_extra_class_attributes)
        return res

    def get_filterset_class(self):
        return type(
            '{}FilterSet'.format(self.filter_model.__name__),
            (django_filters.FilterSet,),
            self.filterset_class_attributes
        )
