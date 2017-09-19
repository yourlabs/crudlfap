import collections

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
        from crudlfap.routers import Router
        context = dict(
            object=record,
            views=Router.registry[type(record)].get_menu('object'),
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
    slug = 'list'
    table_class = Table

    def dispatch(self, *a, **k):
        if not getattr(self, 'filter_fields', None):
            self.filter_fields = self.fields
        if not getattr(self, 'table_fields', None):
            self.table_fields = self.fields
        return super().dispatch(*a, **k)

    def get_context_data(self, *args, **kwargs):
        c = super().get_context_data(*args, **kwargs)
        c['action_views'] = self.router.get_menu('object')
        return c

    def get_table_class(self):
        list_display_links = getattr(self, 'list_display_links', None)
        if not list_display_links:
            for field in self.table_fields:
                model_field = self.model._meta.get_field(field)
                if isinstance(model_field, models.CharField):
                    list_display_links = [field]
                    break

        attrs = collections.OrderedDict(
                Meta=type(
                    'Meta',
                    (object,),
                    dict(
                        model=self.model,
                        fields=self.fields,
                        ),
                    ),
                )

        attrs.update({
            i: tables.LinkColumn() for i in list_display_links
        })

        attrs.update(dict(
            crudlfap=tables.TemplateColumn(
                template_name='crudlfap/_actions.html',
                verbose_name=_('Actions'),
            ),
        ))

        return type(
            '{}Table'.format(self.model.__name__),
            (self.table_class,),
            attrs
        )

    def get_table_data(self):
        return self.filterset.qs

    def get_filterset_class(self):
        return type(
            '{}FilterSet'.format(self.model.__name__),
            (django_filters.FilterSet,),
            dict(
                Meta=getattr(self, 'filterset_meta', type(
                    'Meta',
                    (object,),
                    dict(
                        model=self.model,
                        fields=self.filter_fields,
                        filter_overrides={
                            models.CharField: {
                               'filter_class': django_filters.CharFilter,
                               'extra': lambda f: {
                                   'lookup_expr': 'icontains',
                               },
                           },
                        }
                    )
                ))
            )
        )
