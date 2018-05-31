import collections

from django import template
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import django_tables2 as tables
from django_tables2.config import RequestConfig


class JinjaColumn(tables.Column):
    empty_values = ()

    def __init__(self, template_code, **kwargs):
        self.template_code = template_code
        kwargs.setdefault('default', True)
        super().__init__(**kwargs)

    def render(self, record, table, value, **kwargs):
        from ..site import site
        context = dict(
            object=record,
            request=table.request,
            views=site[type(record)].get_menu(
                'object',
                table.request,
                object=record
            )
        )
        b = template.engines['backend']
        t = b.from_string(self.template_code)
        r = t.render(context)
        return mark_safe(r)


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
                for f in self.model._meta.fields
                if f.name in self.table_sequence
            ]
        else:
            self.table_fields = [
                f.name
                for f in self.model._meta.fields
                if f.name not in self.exclude
            ]
        return self.table_fields

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
            crudlfap=JinjaColumn(
                template_code='''
                {% import 'crudlfap.html' as crudlfap %}
                {{ crudlfap.dropdown(
                    views,
                    'row-actions-' + str(object.pk),
                    class='btn-floating red',
                    next=request.path_info,
                ) }}
                ''',
                verbose_name=_('Actions'),
                orderable=False,
            )
        )

    def get_table_meta_checkbox_column_template(self):
        return '''
            <label>
                <input
                    type="checkbox"
                    data-controller="listaction"
                    data-action="change->listaction#checkboxChange"
                    data-pk="{{ record.pk }}"
                />
                <span></span>
            </label>
        '''

    def get_table_meta_checkbox_column_verbose_name(self):
        return '''
            <label>
                <input
                    type="checkbox"
                    data-controller="listaction"
                    data-action="change->listaction#selectAllChange"
                    data-master="1"
                />
                <span></span>
            </label>
        '''

    def get_table_meta_checkbox_column(self):
        if not self.listactions:
            return dict()

        return dict(
            crudlfap_checkbox=tables.TemplateColumn(
                self.table_meta_checkbox_column_template,
                verbose_name=mark_safe(
                    self.table_meta_checkbox_column_verbose_name
                ),
                orderable=False,
            )
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

        if self.listactions:
            if 'sequence' in attrs:
                attrs['sequence'] = list(attrs['sequence'])
                attrs['sequence'].insert(0, 'crudlfap_checkbox')
                attrs['sequence'].append('crudlfap')
            else:
                attrs['sequence'] = ['crudlfap_checkbox', '...', 'crudlfap']

        return attrs

    def get_table_meta_class(self):
        return type('Meta', (object,), self.table_meta_attributes)

    def get_table_class_attributes(self):
        attrs = collections.OrderedDict(
            Meta=self.table_meta_class,
        )
        attrs.update(self.table_meta_checkbox_column)
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

    def get_paginate_by(self):
        return 10
