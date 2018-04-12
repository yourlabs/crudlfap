"""
Crudlfa+ generic views and mixins.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""
from crudlfap.route import Route

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin


class DefaultTemplateMixin(object):
    """
    Override for get_template_names to append default_template_name.

    This allows to configure "last resort" templates for each class, and thus
    to provide a working CRUD out of the box.
    """

    style = 'default'
    fa_icon = 'question'
    material_icon = 'priority high'
    ajax = '#ajax-container'

    def get_title(self):
        return _(self.urlname).capitalize()

    def get_title_html(self):
        """Return text for HTML title tag."""
        return self.title

    def get_title_heading(self):
        """Return text for page heading."""
        return self.title

    def get_template_names(self):
        """Give a chance to default_template_name."""
        template_names = super().get_template_names()
        default_template_name = getattr(self, 'default_template_name', None)
        if default_template_name:
            template_names.append(default_template_name)
        return template_names


class ViewMixin(DefaultTemplateMixin, Route):
    """Base View mixin for CRUDLFA+.

    If you have any question about style then find your answers in
    DefaultTemplateMixin, otherwise in RoutableViewMixin.
    """
    def get_menu(self):
        return None

    def get_menu_kwargs(self):
        return dict()

    def get_menu_views(self):
        return [
            view
            for view in self.router.get_menu(
                self.menu,
                self.request,
                **self.menu_kwargs
            ) if view.urlname != self.urlname
        ]


class View(ViewMixin, generic.View):
    """Base view for CRUDLFA+."""


class TemplateView(ViewMixin, generic.TemplateView):
    """TemplateView for CRUDLFA+."""


class ModelViewMixin(ViewMixin):
    """Mixin for views using a Model class but no instance."""

    menus = ['model']
    menu = 'model'
    pluralize = False
    object_permission_check = False

    def get_exclude(self):
        return []

    def get_required_permissions(self):
        return [
            '{}.{}_{}'.format(
                self.urlname,
                self.app_name,
                self.model._meta.model_name
            )
        ]

    def get_fields(self):
        return [
            f for f in self.router.get_fields_for_user(
                self.request.user,
                self.required_permissions
            ) if f not in self.exclude
        ]

    def get_model_verbose_name(self):
        if self.pluralize:
            return self.model._meta.verbose_name_plural
        else:
            return self.model._meta.verbose_name

    def get_title(self):
        return '{} {}'.format(
            _(self.urlname),
            self.model_verbose_name,
        ).capitalize()

    def get_queryset(self):
        """Return router.get_queryset() by default, otherwise super()."""
        return self.router.get_objects_for_user(
            self.request.user,
            self.required_permissions,
        )


class ObjectMixin(object):
    """
    Make self.object call and cache self.get_object() automatically.

    WHAT A RELIEF

    However, if it has a router with the get_object() method, use it.
    """

    def get_object(self):
        """Return router.get_object() by default, otherwise super()."""
        router = getattr(self, 'router', None)
        if router and getattr(router, 'get_object', None):
            return router.get_object(self)

        if getattr(self, 'kwargs', False) is False:
            # This happens when the view has not been instanciated with an
            # object, neither from a URL which would allow getting the object
            # in the super() call below.
            raise Exception('Must instanciate the view with an object')
        return super().get_object()

    def object_get(self):
        """Return the object, uses get_object() if necessary."""
        cached = getattr(self, '_object', None)
        if not cached:
            self._object = self.get_object()
        return self._object

    def object_set(self, value):
        """Set self.object attribute."""
        self._object = value

    object = property(object_get, object_set)


class ObjectViewMixin(ObjectMixin, ModelViewMixin, SingleObjectMixin):
    """Mixin for views using a Model instance."""

    menus = ['object']
    menu = 'object'
    object_permission_check = True

    def get_urlargs(self):
        """Return list with object's urlfield attribute."""
        return [getattr(self.object, self.urlfield)]

    def get_slug_field(self):
        """Replace Django's get_slug_field with get_url_field."""
        return self.urlfield

    @property
    def slug_url_kwarg(self):
        """Replace Django's slug_url_kwarg with get_url_field."""
        return self.urlfield

    @classmethod
    def to_url_args(cls, *args):
        """Return first arg's url_field attribute."""
        url_field = cls.get_url_field()
        return [getattr(args[0], url_field)]

    @classmethod
    def get_urlpath(cls):
        """Identify the object by slug or pk in the pattern."""
        return r'<{}>/{}'.format(cls.urlfield, cls.urlname)

    def get_title(self):
        return '{} {} "{}"'.format(
            _(self.urlname),
            self.model_verbose_name,
            self.object
        ).capitalize()

    def get_menu_kwargs(self):
        return dict(object=self.object)


class ObjectView(ObjectViewMixin, View):
    pass


class FormViewMixin(ViewMixin):
    """Mixin for views which have a Form."""
    success_url_next = True

    def get_success_url(self):
        url = super().get_success_url()
        if self.success_url_next and '_next' in self.request.POST:
            url = self.request.POST['_next']
        return url


class FormView(FormViewMixin, generic.FormView):
    """Base FormView class."""

    style = 'warning'
    default_template_name = 'crudlfap/form.html'


class ModelFormViewMixin(ModelViewMixin, FormViewMixin):
    """ModelForm ViewMixin using readable"""

    menus = ['model']

    def get_form_fields(self):
        if hasattr(self.router, 'form_fields'):
            return self.router.form_fields
        if hasattr(self.router, 'fields'):
            return self.router.fields
        return self.get_fields()

    def get_form_class(self):
        if self.fields is None and not self.form_class:
            self.fields = self.form_fields
        return super().get_form_class()

    def get_form_invalid_message(self):
        return '{} {} error'.format(
            self.urlname,
            self.model_verbose_name
        ).capitalize()

    def get_form_valid_message(self):
        return _(
            '%s %s: {}' % (self.urlname, self.model_verbose_name)
        ).format(self.form.instance).capitalize()

    def form_invalid(self, form):
        messages.error(self.request, self.form_invalid_message)
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, self.form_valid_message)
        return super().form_valid(form)


class ObjectFormViewMixin(ObjectViewMixin, ModelFormViewMixin):
    """Custom form view mixin on an object."""


class ObjectFormView(ObjectFormViewMixin, generic.FormView):
    """Custom form view on an object."""


class CreateView(ModelFormViewMixin, generic.CreateView):
    """View to create a model object."""

    style = 'success'
    material_icon = 'add'
    default_template_name = 'crudlfap/create.html'
    controller = 'modal'
    action = 'click->modal#open'
    color = 'green'
    object_permission_check = False

    def get_form_fields(self):
        if hasattr(self, 'create_fields'):
            return self.create_fields
        if hasattr(self.router, 'create_fields'):
            return self.router.create_fields
        return super().get_form_fields()


class DeleteView(ObjectFormViewMixin, generic.DeleteView):
    """View to delete a model object."""

    default_template_name = 'crudlfap/delete.html'
    style = 'danger'
    fa_icon = 'trash'
    material_icon = 'delete'
    success_url_next = True
    controller = 'modal'
    action = 'click->modal#open'
    color = 'red'

    def get_success_message(self):
        return _(
            '%s %s: {}' % (self.urlname, self.model_verbose_name)
        ).format(self.object).capitalize()

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.router['list'].reverse()

    def get_required_permissions(self):
        return ['{}.delete_{}'.format(
            self.app_name, self.model._meta.model_name)]


class DetailView(ObjectViewMixin, generic.DetailView):
    """Templated model object detail view which takes a field option."""

    fa_icon = 'search-plus'
    material_icon = 'search'
    default_template_name = 'crudlfap/detail.html'
    color = 'blue'

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


class ListView(ModelViewMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'crudlfap/list.html'
    urlpath = ''
    fa_icon = 'table'
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


class UpdateView(ObjectFormViewMixin, generic.UpdateView):
    """Model update view."""

    material_icon = 'edit'
    default_template_name = 'crudlfap/update.html'
    controller = 'modal'
    action = 'click->modal#open'
    color = 'orange'

    def get_form_fields(self):
        if hasattr(self, 'update_fields'):
            return self.update_fields
        if hasattr(self.router, 'update_fields'):
            return self.router.update_fields
        return super().get_form_fields()

    def get_required_permissions(self):
        return ['{}.change_{}'.format(
            self.app_name, self.model._meta.model_name)]
