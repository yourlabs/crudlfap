import collections

from betterforms.changelist import SearchForm

from django import forms
from django import template
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.utils.safestring import mark_safe

import django_filters

import django_tables2 as tables
from django_tables2.config import RequestConfig

from ..site import site
from .generic import ObjectFormViewMixin, ModelViewMixin


class JinjaColumn(tables.Column):
    empty_values = ()

    def __init__(self, template_code, **kwargs):
        self.template_code = template_code
        kwargs.setdefault('default', True)
        super().__init__(**kwargs)

    def render(self, record, table, value, **kwargs):
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

    def get_listactions(self):
        return self.router.get_menu('list_action', self.request)


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
            crudlfap=JinjaColumn(
                template_code='''
                {% import 'crudlfap.html' as crudlfap %}
                {{ crudlfap.dropdown(
                    views,
                    'row-actions-' + str(object.pk),
                    class='btn-floating red',
                ) }}
                ''',
                verbose_name=_('Actions'),
                orderable=False,
            )
        )

    def get_table_meta_checkbox_column(self):
        if not self.listactions:
            return dict()

        return dict(
            crudlfap_checkbox=tables.TemplateColumn(
                '''
                <label>
                    <input
                        type="checkbox"
                        data-controller="listaction"
                        data-action="change->listaction#checkboxChange"
                        data-pk="{{ record.pk }}"
                    />
                    <span></span>
                </label>
                ''',
                verbose_name=mark_safe('''
                <label>
                    <input
                        type="checkbox"
                        data-controller="listaction"
                        data-action="change->listaction#selectAllChange"
                        data-master="1"
                    />
                    <span></span>
                </label>
                '''),
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


class BaseListView(ModelViewMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'crudlfap/list.html'
    material_icon = 'list'
    menus = ['main', 'model']
    pluralize = True

    def get(self, *a, **k):
        '''Enforce sane default paginate_by if not False.'''
        if getattr(self, 'paginate_by', None) is None:
            self.paginate_by = self.get_paginate_by()
        return super().get(*a, **k)

    def get_paginate_by(self, queryset=None):
        if self.router and hasattr(self.router, 'paginate_by'):
            return self.router.paginate_by

        return 10


class ObjectsFormViewMixin(ObjectFormViewMixin):
    pluralize = True

    def get_queryset(self):
        return super().get_queryset().filter(
            pk__in=self.request.GET.getlist('pks')
        )

    def form_valid(self, form):
        for obj in self.object_list:
            self.object = obj
            response = super().form_valid(form)
        return response


class ObjectsFormView(ObjectFormViewMixin, BaseListView):
    pass


class ListView(SearchMixin, FilterMixin, TableMixin, BaseListView):
    default_template_name = 'crudlfap/list.html'
    body_class = 'full-width'
    urlpath = ''

    def get_title_heading(self):
        return self.model._meta.verbose_name_plural.capitalize()

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
