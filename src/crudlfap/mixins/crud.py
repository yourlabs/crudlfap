"""CRUD :eMixins that can be used in Actions or Views."""
import copy
import json

from django import forms
from django import http
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.contenttypes.models import ContentType

from crudlfap import html


class CreateMixin:
    style = 'success'
    icon = 'add'
    default_template_name = 'crudlfap/create.html'
    template_name_suffixes = ['create', 'form']
    controller = 'modal'
    action = 'click->modal#open'
    color = 'green'
    log_action_flag = ADDITION
    menus = ['model']
    permission_shortcode = 'add'

    def form_valid(self):
        self.object = self.form.save()
        return super().form_valid()


class ActionMixin:
    def has_perm(self):
        """
        Call has_perm_object or return True.

        When called without an object, return True if router agrees.

        Otherwise, return the result of has_perm_object(), that you must
        implement, to return wether permission is accepted for a particular
        object.

        To override yourself, again go inside an if super().has_perm(): to
        benefit from this behaviour.
        """
        if super().has_perm():
            if hasattr(self, 'object'):
                return self.has_perm_object()
            return True

    def has_perm_object(self):
        """
        Override this method: test self.object then return True.

        By default, return True.
        """
        return True


class DeleteMixin(ActionMixin):
    style = 'danger'
    fa_icon = 'trash'
    icon = 'delete'
    success_url_next = True
    color = 'red'
    log_action_flag = DELETION
    controller = 'modal'
    action = 'click->modal#open'
    form_class = forms.Form
    permission_shortcode = 'delete'

    def form_valid(self):
        if hasattr(self, 'object_list'):
            self.result = copy.copy(self.object_list).delete()
        else:
            self.result = self.object.delete()
        return super().form_valid()

    def get_success_url(self):
        return self.router['list'].reverse()


class DetailMixin:
    fa_icon = 'search-plus'
    icon = 'search'
    default_template_name = 'crudlfap/detail.html'
    color = 'blue'
    menus_display = ['object', 'object_detail']

    @classmethod
    def get_urlpath(cls):
        """Identify the object by slug or pk in the pattern."""
        return r'<{}>'.format(cls.urlfield)

    def get_JSONField_display(self, name):  # noqa
        value = getattr(self.object, name, "")
        formated = json.dumps(value, indent=4)
        return f'<pre>{formated}</pre>'

    def get_title(self):
        return str(self.object)

    def get_visible_fields(self):
        return [
            f.name for f in self.model._meta.fields
            if self.fields == '__all__' or f.name not in self.exclude
        ]

    def get_display_fields(self):
        """Table field rendering"""
        self.display_fields = [
            {
                'field': self.model._meta.get_field(field),
                'value': self.get_field_display(field),
                'name': field,
            }
            for field in self.visible_fields
        ]

    def get_field_display(self, name):
        value_getter = '_'.join(['get', name, 'display'])
        if hasattr(self.object, value_getter):
            return getattr(self.object, value_getter)()
        if hasattr(self, value_getter):
            return getattr(self, value_getter)()
        type_getter = '_'.join([
            'get',
            type(self.model._meta.get_field(name)).__name__,
            'display',
        ])
        if hasattr(self, type_getter):
            return getattr(self, type_getter)(name)
        value = getattr(self.object, name)
        if hasattr(value, 'get_absolute_url'):
            return html.A(
                str(value),
                href=value.get_absolute_url(),
            ).render()
        return value

    def get_json_fields(self):
        return self.visible_fields

    def get_FIELD_json(self, obj, field):
        value = getattr(obj, field)
        if self.router and type(value) in self.router.registry:
            value = self.router.registry[type(value)].serialize(obj)
        elif value and not isinstance(value, (str, int, float, bool)):
            value = str(value)
        return value

    def serialize(self):
        if self.router:
            return self.router.serialize(self.object, self.json_fields)
        return {
            field: getattr(
                self,
                f'get_{field}_json',
                'get_FIELD_json',
            )(self.object, field)
            for field in self.json_fields
        }

    def json_get(self, request, *args, **kwargs):
        return http.JsonResponse(self.serialize())


class HistoryMixin:
    icon = 'history'
    template_name_suffix = '_history'
    default_template_name = 'crudlfap/history.html'
    controller = None
    action = None

    def get_object_list(self):
        ctype = ContentType.objects.get_for_model(self.model)
        return LogEntry.objects.filter(
            content_type=ctype,
            object_id=self.object.pk,
        )


class ListMixin:
    default_template_name = 'crudlfap/list.html'
    body_class = 'full-width'
    menus = ['main', 'model']
    title_heading = None

    def get_icon(self):
        if self.router:
            return self.router.icon
        return 'list'

    def get_title(self):
        return self.model._meta.verbose_name_plural.capitalize()

    def get_urlpath(self):
        return ''

    def get_title_heading(self):
        return self.model._meta.verbose_name_plural.capitalize()

    def get_swagger_get(self):
        '''TODO
        parameters = {
                    'collectionFormat': 'multi',
                    'description': 'Status values to filter',
                    'in': 'query',
                    'items': {
                        'default': 'available',
                        'enum': ['available', 'pending', 'sold'],
                        'type': 'string'
                    },
                    'name': 'status',
                    'required': True,
                    'type': 'array'
                }
        '''
        return {
            # 'description': self.title,
            # 'operationId': 'findPetsByStatus',
            'parameters': [],
            'produces': ['application/json'],
            'responses': {
                '200': {
                    'description': 'successful operation',
                    'schema': {
                        'items': {
                            '$ref': '#/definitions/' + self.model.__name__
                        },
                        'type': 'array'
                    }
                },
                '400': {'description': 'Invalid status value'}
            },
            'summary': self.title,
            'tags': self.swagger_tags
        }


class UpdateMixin:
    icon = 'edit'
    default_template_name = 'crudlfap/update.html'
    template_name_suffixes = ['create', 'form']
    controller = 'modal'
    action = 'click->modal#open'
    color = 'orange'
    locks = True
    log_action_flag = CHANGE
    permission_shortcode = 'change'

    def get_form_fields(self):
        if hasattr(self, 'update_fields'):
            return self.update_fields
        if hasattr(self.router, 'update_fields'):
            return self.router.update_fields
        return super().get_form_fields()

    def form_valid(self):
        self.object = self.form.save()
        return super().form_valid()
