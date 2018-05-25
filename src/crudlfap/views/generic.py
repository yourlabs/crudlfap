"""
Crudlfa+ generic views and mixins.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""
from django.conf import settings
from django.contrib.admin.models import ADDITION
from django.contrib.contenttypes.models import ContentType
from django.views import generic
from django.views.generic.detail import SingleObjectMixin, BaseDetailView

from ..route import Route
from .. import mixins


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


class ObjectView(mixins.ObjectMixin, TemplateView):
    pass


class FormView(mixins.FormMixin, TemplateView):
    """Base FormView class."""

    style = 'warning'
    default_template_name = 'crudlfap/form.html'


class ModelFormView(mixins.ModelFormMixin, FormView):
    pass


class ObjectFormView(mixins.ObjectFormMixin, FormView):
    """Custom form view on an object."""


class CreateView(mixins.ModelFormMixin, TemplateView, generic.CreateView):
    """View to create a model object."""

    style = 'success'
    material_icon = 'add'
    default_template_name = 'crudlfap/create.html'
    controller = 'modal'
    action = 'click->modal#open'
    color = 'green'
    object_permission_check = False
    log_action_flag = ADDITION

    def get_form_fields(self):
        if hasattr(self, 'create_fields'):
            return self.create_fields
        if hasattr(self.router, 'create_fields'):
            return self.router.create_fields
        return super().get_form_fields()


class DetailView(ObjectView, BaseDetailView):
    """Templated model object detail view which takes a field option."""

    fa_icon = 'search-plus'
    material_icon = 'search'
    default_template_name = 'crudlfap/detail.html'
    color = 'blue'
    menus_display = ['object', 'object_detail']

    def get_title(self):
        return str(self.object)

    def get_context_data(self, *a, **k):
        c = super(DetailView, self).get_context_data(*a, **k)
        c['fields'] = [
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
        return c

    @classmethod
    def get_urlpath(cls):
        """Identify the object by slug or pk in the pattern."""
        return r'<{}>'.format(cls.urlfield)

    def get_required_permissions(self):
        return ['{}.detail_{}'.format(
            self.app_name, self.model._meta.model_name)]


class HistoryView(mixins.ObjectMixin, generic.DetailView):
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


class ListView(mixins.SearchMixin, mixins.FilterMixin, mixins.TableMixin,
               mixins.ObjectsMixin, TemplateView):

    default_template_name = 'crudlfap/list.html'
    material_icon = 'list'
    body_class = 'full-width'
    menus = ['main', 'model']

    def get_urlpath(self):
        return ''

    def get_title_heading(self):
        return self.model._meta.verbose_name_plural.capitalize()

    def get_object_list(self):
        if self.filterset:
            object_list = self.filterset.qs
        else:
            object_list = self.queryset

        if self.search_fields:
            self.search_form = self.get_search_form()
            object_list = self.search_form.get_queryset()
        return object_list


class ObjectsFormView(mixins.ObjectsFormMixin, TemplateView):
    pass


class UpdateView(mixins.ObjectFormMixin, mixins.TemplateMixin,
                 generic.UpdateView):
    """Model update view."""

    material_icon = 'edit'
    default_template_name = 'crudlfap/update.html'
    controller = 'modal'
    action = 'click->modal#open'
    color = 'orange'
    locks = True

    def get_form_fields(self):
        if hasattr(self, 'update_fields'):
            return self.update_fields
        if hasattr(self.router, 'update_fields'):
            return self.router.update_fields
        return super().get_form_fields()

    def get_required_permissions(self):
        return ['{}.change_{}'.format(
            self.app_name, self.model._meta.model_name)]
