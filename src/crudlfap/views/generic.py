"""
Crudlfa+ generic views and mixins.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""
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


class UpdateView(mixins.UpdateMixin, ObjectFormView):
    """Model update view."""
