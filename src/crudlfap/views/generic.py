"""
Crudlfa+ generic views and mixins.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""
from django import http
from django.conf import settings
from django.views import generic

from .. import mixins
from ..route import Route

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib.admin.models import LogEntry
else:
    LogEntry = None


class View(mixins.LockMixin, mixins.MenuMixin, Route, generic.View):
    """Base view for CRUDLFA+."""


class TemplateView(mixins.TemplateMixin, View):
    """TemplateView for CRUDLFA+."""


class ModelView(mixins.ModelMixin, TemplateView):
    pass


class ObjectFormView(mixins.ObjectFormMixin, TemplateView):
    """Custom form view on an object."""


class ObjectView(mixins.ObjectMixin, TemplateView):
    pass


class ObjectsFormView(mixins.ObjectsFormMixin, TemplateView):
    pass


class ObjectsView(mixins.ObjectsMixin, TemplateView):
    pass


class FormView(mixins.FormMixin, TemplateView):
    """Base FormView class."""

    style = 'warning'
    default_template_name = 'crudlfap/form.html'


class ModelFormView(mixins.ModelFormMixin, FormView):
    pass


class CreateView(mixins.CreateMixin, ModelFormView):
    """View to create a model object."""


class DeleteView(mixins.DeleteMixin, ObjectFormView):
    """View to delete an object."""


class DeleteObjectsView(mixins.DeleteMixin, ObjectsFormView):
    """Delete selected objects."""


class DetailView(mixins.DetailMixin, ObjectView):
    """Templated model object detail view which takes a field option."""

    def get_swagger_summary(self):
        return f'{self.model.__name__} Detail'

    def get_swagger_get(self):
        result = {
            'operationId': f'find{self.model.__name__}ByStatus',
            'produces': ['application/json'],
            'responses': {
                '200': {
                    'description': 'successful operation',
                    'schema': {
                        'items': {
                            '$ref': f'#/definitions/{self.model.__name__}'
                        },
                        'type': 'array'
                    }
                },
                '404': {
                    'description': 'Not found'
                },
            },
            'summary': self.swagger_summary,
            'tags': self.swagger_tags,
        }
        return result


class HistoryView(mixins.ObjectMixin, generic.DetailView):
    pass


class ListView(mixins.ListMixin, mixins.SearchMixin, mixins.FilterMixin,
               mixins.TableMixin, mixins.ObjectsMixin, TemplateView):

    def get_object_list(self):
        if self.filterset:
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.queryset

        if self.search_form:
            self.object_list = self.search_filter(self.object_list)

        return self.object_list

    def get_listactions(self):
        return self.router.get_menu('list_action', self.request)

    def get_swagger_get(self):
        parameters = []
        if self.filterset:
            for name, field in self.filterset.form.fields.items():
                parameters.append({
                    'collectionFormat': 'single',
                    'description': field.help_text,
                    'in': 'query',
                    'name': name,
                    'required': field.required,
                    'type': 'string'
                })

        return {
            # 'description': 'Multiple status are comma separated',
            'operationId': f'find{self.model.__name__}ByStatus',
            'parameters': parameters,
            'produces': ['application/json'],
            'responses': {
                '200': {
                    'description': 'successful operation',
                    'schema': {
                        'items': {
                            '$ref': f'#/definitions/{self.model.__name__}'
                        },
                        'type': 'array'
                    }
                },
                '400': {'description': 'Invalid parameter'}
            },
            'summary': self.title,
            'tags': self.swagger_tags,
        }

    def json_get(self, request, *args, **kwargs):
        rows = []
        for row in self.table.paginated_rows:
            json_row = dict()
            for field in self.table_fields:
                value = getattr(row.record, field, None)
                if not isinstance(value, (str, int, float, bool, None)):
                    value = str(value)
                json_row[field] = value
            rows.append(json_row)
        data = dict(
            results=rows,
            paginator=dict(
                page_number=self.table.page.number,
                per_page=self.table.page.paginator.per_page,
                total_pages=self.table.page.paginator.num_pages,
                total_objects=self.table.page.paginator.count,
                has_next=self.table.page.has_next(),
                has_previous=self.table.page.has_previous(),
            )
        )
        return http.JsonResponse(data)


class UpdateView(mixins.UpdateMixin, ObjectFormView):
    """Model update view."""
