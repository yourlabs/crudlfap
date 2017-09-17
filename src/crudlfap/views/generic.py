"""
Crudlfa+ generic views and mixins.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""
from django.conf.urls import url
from django.core.exceptions import FieldDoesNotExist
from django.views import generic


class ViewMixin(object):
    """
    Mixin to make crudlfa+ love a view.

    .. py:attribute:: slug

        Slug name of this view, often properly automatically generated
        from view class name uppon registration.

    .. py:attribute:: verbose_slug

        Verbose slug of the view for display.

    .. py:attribute:: url_pattern

        URL pattern to use for this view.
    """

    slug = None
    url_pattern = None

    @property
    def verbose_slug(self):
        """Translate and capitalize slug for display."""
        from django.utils.translation import ugettext_lazy as _
        from django.template import defaultfilters
        return defaultfilters.capfirst(_(self.slug))

    @classmethod
    def as_url(cls, **kwargs):
        """Return the Django url object."""
        return url(
            '{}{}'.format(
                cls.router.prefix or '',
                cls.get_url_pattern(),
            ),
            cls.as_view(**kwargs),
            name=cls.get_url_name(),
        )

    @classmethod
    def get_url_pattern(cls):
        """Return the url pattern for this view."""
        if cls.url_pattern:
            return cls.url_pattern.format(cls.slug)
        return '{}/$'.format(cls.slug)

    @classmethod
    def get_url_name(cls):
        """Return the url name for this view which has a router."""
        return '{}_{}'.format(
            cls.router.model_name,
            cls.slug,
        )

    @classmethod
    def get_url_args(cls, *args):  # pylint: disable=unused-argument
        """Return url reverse args given these args."""
        return []

    @classmethod
    def reverse(cls, *args):
        """Reverse a url to this view with the given args."""
        from django.core.urlresolvers import reverse_lazy
        return reverse_lazy(
            cls.get_url_name(*args),
            args=cls.get_url_args(*args)
        )


class View(ViewMixin, generic.View):
    """Base view for crudlfap+."""


class ModelViewMixin(ViewMixin):
    """Mixin for views using a Model class but no instance."""


class ObjectViewMixin(ViewMixin):
    """Mixin for views using a Model instance."""

    @classmethod
    def get_url_pattern(cls):
        """Identify the object by slug or pk in the pattern."""
        if cls.url_pattern:
            return cls.url_pattern.format(cls.slug)

        try:
            cls.model._meta.get_field('slug')
        except FieldDoesNotExist:
            return r'(?P<pk>\d+)/{}/$'.format(cls.slug)
        else:
            return r'(?P<slug>[\w\d_-]+)/{}/$'.format(cls.slug)


class FormViewMixin(ViewMixin):
    """Mixin for views which have a Form."""


class FormView(FormViewMixin, generic.FormView):
    """Base FormView class."""

    style = 'warning'
    default_template_name = 'crudlfap/form.html'


class ObjectFormView(ObjectViewMixin, FormViewMixin, generic.FormView):
    """Custom form view on an object."""


class CreateView(ModelViewMixin, FormViewMixin, generic.CreateView):
    """View to create a model object."""

    style = 'success'
    icon = 'fa fa-fw fa-plus'
    menus = ['list_action']
    default_template_name = 'crudlfap/create.html'
    target = 'modal'


class DeleteView(ObjectViewMixin, generic.DeleteView):
    """View to delete a model object."""

    default_template_name = 'crudlfap/delte.html'
    style = 'danger'
    icon = 'fa fa-fw fa-trash'
    target = 'modal'


class DetailView(ObjectViewMixin, generic.DetailView):
    """Model object detail view."""

    default_template_name = 'crudlfap/detail.html'


class ListView(ModelViewMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'crudlfap/list.html'
    url_pattern = '$'


class UpdateView(ObjectViewMixin, generic.UpdateView):
    """Model update view."""

    default_template_name = 'crudlfap/update.html'
