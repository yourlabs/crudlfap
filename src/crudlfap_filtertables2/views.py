import collections

from betterforms.changelist import SearchForm
from crudlfap.views.generic import ListView

from django import template
from django.db import models
from django.utils.translation import ugettext_lazy as _

import django_filters
from django_filters.views import FilterView

import django_tables2 as tables
from django_tables2.views import SingleTableMixin


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


class FilterTables2ListView(SingleTableMixin, FilterView, ListView):
    urlre = r'$'
    default_template_name = 'crudlfap_filtertables2/list.html'
    template_name_suffix = '_list'
    icon = 'fa fa-fw fa-table'
    urlname = 'list'
    table_class = Table

    def get_table_fields(self):
        return [
            f.name
            for f in self.model._meta.fields
            if f.name not in self.exclude
        ]

    def get_table_link_fields(self):
        for field in self.table_fields:
            model_field = self.model._meta.get_field(field)
            if isinstance(model_field, models.CharField):
                return [field]

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

    def get_table_meta_attributes(self):
        return dict(model=self.model, fields=self.table_fields)
        return attrs

    def get_table_meta_class(self):
        return type('Meta', (object,), self.table_meta_attributes)

    def get_table_class_attributes(self):
        attrs = collections.OrderedDict(
            Meta=self.table_meta_class,
        )
        attrs.update(self.table_meta_link_columns)
        attrs.update(self.table_meta_action_columns)
        return attrs

    def get_table_class(self):
        return type(
            '{}Table'.format(self.model.__name__),
            (self.table_class,),
            self.table_class_attributes
        )

    def get_table_data(self):
        if self.search_form.is_valid():
            return self.search_form.get_queryset()
        return self.filterset.qs

    def get_search_form_class(self):
        if not self.search_fields:
            return

        return type(
            self.model.__name__ + 'SearchForm',
            (SearchForm,),
            dict(
                SEARCH_FIELDS=self.search_fields,
                model=self.model
            )
        )

    def get_search_form(self):
        if SearchForm:
            form = self.search_form_class(
                self.request.GET,
                queryset=self.filterset.qs
            )
            form.full_clean()
            return form

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
