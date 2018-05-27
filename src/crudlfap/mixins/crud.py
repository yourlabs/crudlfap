"""CRUD :eMixins that can be used in Actions or Views."""
from django import forms
from django import http
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


class CreateMixin:
    style = 'success'
    material_icon = 'add'
    default_template_name = 'crudlfap/create.html'
    controller = 'modal'
    action = 'click->modal#open'
    color = 'green'
    object_permission_check = False
    log_action_flag = ADDITION
    menus = ['main', 'model']


class DeleteMixin:
    default_template_name = 'crudlfap/delete.html'
    style = 'danger'
    fa_icon = 'trash'
    material_icon = 'delete'
    success_url_next = True
    color = 'red'
    log_action_flag = DELETION
    controller = 'modal'
    action = 'click->modal#open'
    form_class = forms.Form
    menus = ['object', 'object_detail']

    def get_success_url(self):
        return self.router['list'].reverse()


class DetailMixin:
    fa_icon = 'search-plus'
    material_icon = 'search'
    default_template_name = 'crudlfap/detail.html'
    color = 'blue'
    menus_display = ['object', 'object_detail']

    @classmethod
    def get_urlpath(cls):
        """Identify the object by slug or pk in the pattern."""
        return r'<{}>'.format(cls.urlfield)

    def get_title(self):
        return str(self.object)

    def get_display_fields(self):
        self.display_fields = [
            {
                'field': self.model._meta.get_field(field),
                'value': getattr(self.object, field)
            }
            for field in (
                [f.name for f in self.model._meta.fields]
                if self.fields == '__all__'
                else self.fields
            ) if field not in self.exclude
        ]
        return self.display_field


class HistoryMixin:
    material_icon = 'history'
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
    material_icon = 'list'
    body_class = 'full-width'
    menus = ['main', 'model']

    def get_urlpath(self):
        return ''

    def get_title_heading(self):
        return self.model._meta.verbose_name_plural.capitalize()


class UpdateMixin:
    material_icon = 'edit'
    default_template_name = 'crudlfap/update.html'
    controller = 'modal'
    action = 'click->modal#open'
    color = 'orange'
    locks = True
    log_action_flag = CHANGE

    def get_form_fields(self):
        if hasattr(self, 'update_fields'):
            return self.update_fields
        if hasattr(self.router, 'update_fields'):
            return self.router.update_fields
        return super().get_form_fields()
