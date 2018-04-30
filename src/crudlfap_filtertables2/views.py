import collections

from betterforms.changelist import SearchForm
from crudlfap.views.generic import ListView

from django import forms
from django import template
from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_filters
from django_filters.filterset import filterset_factory

import django_tables2 as tables
from django_tables2.config import RequestConfig


class Table(tables.Table):
    def render_crudlfap(self, record):
        from django.template import loader
        from crudlfap import crudlfap
        context = dict(
            object=record,
            views=crudlfap.site[type(record)].get_menu(
                'object',
                self.context['request'],
                object=record,
            ),
            extra_class='btn-small secondary-content'
        )
        template = loader.select_template([
            '{}/_{}_actions.html'.format(
                type(record)._meta.app_label,
                type(record)._meta.model_name,
                ),
            'crudlfap/_actions.html',
            ])
        return template.render(context)

    def render_tags(self, record):
        html = []
        for tag in record.tags.all():
            html.append(unicode(tag))

        return ' '.join(html)


class FilterMixin(object):
    def get_filterset_class(self):
        return filterset_factory(model=self.model, fields=self.filter_fields)

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
            'queryset': self.get_queryset(),
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


class TableMixin(object):
    def get_table_fields(self):
        if self.table_sequence:
            return [
                f.name
                for f in self.model._meta.fields
                if f.name in self.table_sequence
            ]

        return [
            f.name
            for f in self.model._meta.fields
            if f.name not in self.exclude
        ]

    def get_table_link_fields(self):
        if not hasattr(self.model, 'get_absolute_url'):
            return []

        for field in self.table_fields:
            model_field = self.model._meta.get_field(field)
            if isinstance(model_field, models.CharField):
                return [field]

        return []

    def get_table_meta_link_columns(self):
        return {i: tables.LinkColumn() for i in self.table_link_fields}

    def get_table_meta_action_columns(self):
        return dict(
            crudlfap=tables.TemplateColumn(
                template_name='crudlfap/_actions.html',
                verbose_name=_('Actions'),
                extra_context=dict(extra_class='btn-small'),
                orderable=False,
            ),
        )

    def get_table_sequence(self):
        return None

    def get_table_columns(self):
        return dict()

    def get_table_meta_attributes(self):
        attrs = dict(model=self.model)

        if self.table_sequence:
            attrs['sequence'] = self.table_sequence

        if self.table_fields:
            attrs['fields'] = self.table_fields

        return attrs

    def get_table_meta_class(self):
        return type('Meta', (object,), self.table_meta_attributes)

    def get_table_class_attributes(self):
        attrs = collections.OrderedDict(
            Meta=self.table_meta_class,
        )
        attrs.update(self.table_meta_link_columns)
        attrs.update(self.table_meta_action_columns)
        attrs.update(self.table_columns)
        return attrs

    def get_table_class(self):
        return Table

    def build_table_class(self):
        bases = (self.table_class,)
        if (self.table_class != Table
                and not issubclass(self.table_class, Table)):

            bases = (self.table_class, Table)

        return type(
            '{}Table'.format(self.model.__name__),
            bases,
            self.table_class_attributes
        )

    def get_table_kwargs(self):
        return {}

    def get_table_pagination(self):
        if not self.paginate_by:
            return True
        return dict(per_page=self.paginate_by)

    def get_table(self):
        kwargs = self.table_kwargs
        kwargs.update(data=self.object_list)
        self.table = self.build_table_class()(**kwargs)
        RequestConfig(
            self.request,
            paginate=self.table_pagination,
        ).configure(self.table)
        return self.table


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


class FilterTables2ListView(SearchMixin, FilterMixin, TableMixin, ListView):
    urlre = r'$'
    default_template_name = 'crudlfap_filtertables2/list.html'
    icon = 'fa fa-fw fa-table'
    urlname = 'list'

    def get(self, request, *args, **kwargs):
        if self.filterset:
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.get_queryset()

        if self.search_fields:
            self.search_form = self.get_search_form()
            self.object_list = self.search_form.get_queryset()

        # Trick super()
        self.get_queryset = lambda *a: self.object_list
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        if self.search_fields:
            form = self.search_form_class(
                self.request.GET,
                queryset=self.object_list
            )
            form.full_clean()
            return form
