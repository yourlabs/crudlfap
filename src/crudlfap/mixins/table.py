import collections

import django_tables2 as tables
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_tables2.config import RequestConfig

from crudlfap import html


class UnpolyLinkColumn(tables.LinkColumn):
    def render(self, record, value):
        return super().render(record, value).replace(
            '<a ',
            '<a up-target="{html.A.attrs["up-target"]}"',
        )


class ActionsColumn(tables.Column):
    empty_values = ()

    def __init__(self, **kwargs):
        kwargs.setdefault('default', True)
        super().__init__(**kwargs)

    def render(self, record, table, value, **kwargs):
        from crudlfap.site import site
        out = html.Div(
            *site[type(record)].get_menu_component(
                'object',
                table.request,
                object=record,
            ).content,
            style='display:flex;flex-direction:row-reverse',
        ).render()
        return mark_safe(out)


class Table(tables.Table):
    def before_render(self, request):
        self.request = request

    def render_tags(self, record):
        html = []
        for tag in record.tags.all():
            html.append(str(tag))

        return ' '.join(html)


class TableMixin(object):
    def get_table_fields(self):
        if self.table_sequence:
            self.table_fields = [
                f.name
                for f in self.object_list.model._meta.fields
                if f.name in self.table_sequence
            ]
        else:
            self.table_fields = [
                f.name
                for f in self.object_list.model._meta.fields
                if f.name not in self.exclude
            ]
        return self.table_fields

    def get_table_link_fields(self):
        if not hasattr(self.object_list.model, 'get_absolute_url'):
            return []

        for field in self.table_fields:
            model_field = self.object_list.model._meta.get_field(field)
            if isinstance(model_field, models.CharField):
                return [field]

        return []

    def get_table_meta_link_columns(self):
        return {i: UnpolyLinkColumn() for i in self.table_link_fields}

    def get_table_meta_action_columns(self):
        return dict(
            crudlfap=ActionsColumn(
                verbose_name=_('Actions'),
                orderable=False,
            )
        )

    def get_table_sequence(self):
        return None

    def get_table_columns(self):
        return dict()

    def get_table_meta_attributes(self):
        attrs = dict(model=self.object_list.model)

        if self.table_sequence:
            attrs['sequence'] = self.table_sequence

        if self.table_fields:
            attrs['fields'] = self.table_fields

        if self.listactions:
            if 'sequence' in attrs:
                attrs['sequence'] = list(attrs['sequence'])
                attrs['sequence'].append('crudlfap')
            else:
                attrs['sequence'] = ['...', 'crudlfap']

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
            '{}Table'.format(self.object_list.model.__name__),
            bases,
            self.table_class_attributes
        )

    def get_table_kwargs(self):
        return dict(data=self.object_list)

    def get_max_per_page(self):
        return 100

    def get_table_pagination(self):
        if not self.paginate_by:
            return True
        per_page = int(self.request.GET.get('per_page', self.paginate_by))
        if per_page > self.max_per_page:
            return self.max_per_page
        return dict(per_page=per_page)

    def get_table(self):
        kwargs = self.table_kwargs
        self.table = self.build_table_class()(**kwargs)
        RequestConfig(
            self.request,
            paginate=self.table_pagination,
        ).configure(self.table)
        return self.table

    def get_paginate_by(self):
        return 10
