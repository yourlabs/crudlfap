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

    def get_template_names(self):
        """Give a chance to default_template_name."""
        template_names = super().get_template_names()
        default_template_name = getattr(self, 'default_template_name', None)
        if default_template_name:
            template_names.append(default_template_name)
        return template_names

    @classmethod
    def get_fa_icon(cls):
        return getattr(cls, 'fa_icon', None) or getattr(cls.router, 'fa_icon', '')

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
        return args

    @classmethod
    def reverse(cls, *args):
        """Reverse a url to this view with the given args."""
        from django.core.urlresolvers import reverse_lazy
        return reverse_lazy(
            cls.get_url_name(),
            args=cls.get_url_args(*args)
        )


class View(ViewMixin, generic.View):
    """Base view for crudlfap+."""


class ModelViewMixin(ViewMixin):
    """Mixin for views using a Model class but no instance."""

    menus = ['model']


class ObjectViewMixin(ViewMixin):
    """Mixin for views using a Model instance."""

    menus = ['object']

    @classmethod
    def get_url_args(cls, *args):
        if '<slug>' in cls.get_url_pattern():
            return [args[0].slug]
        return [args[0].pk]

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


class ModelFormViewMixin(ModelViewMixin, FormViewMixin):
    """ModelForm ViewMixin using readable"""


class ObjectFormView(ObjectViewMixin, FormViewMixin, generic.FormView):
    """Custom form view on an object."""


class CreateView(ModelViewMixin, FormViewMixin, generic.CreateView):
    """View to create a model object."""

    style = 'success'
    fa_icon = 'plus'
    default_template_name = 'crudlfap/create.html'
    target = 'modal'

    @property
    def fields(self):
        return self.router.get_writable_fields(self.request.user)


class DeleteView(ObjectViewMixin, generic.DeleteView):
    """View to delete a model object."""

    default_template_name = 'crudlfap/delte.html'
    style = 'danger'
    fa_icon = 'trash'
    target = 'modal'


class DetailView(ObjectViewMixin, generic.DetailView):
    """Templated model object detail view which takes a field option."""

    default_template_name = 'crudlfap/detail.html'

    @property
    def fields(self):
        return self.router.get_writable_fields(self.request.user)

    def get_context_data(self, *a, **k):
        c = super(DetailView, self).get_context_data(*a, **k)
        return c  # inhiate brokn code
        c['fields'] = [
            {
                'object': self.object,
                'field': field,
                'value': getattr(self.object, field.name)
            }
            for field in self.drycrud.get_readable_fields(self).values()
        ]
        return c


class ListView(ModelViewMixin, generic.ListView):
    """Model list view."""

    default_template_name = 'crudlfap/list.html'
    url_pattern = '$'


class UpdateView(ObjectViewMixin, generic.UpdateView):
    """Model update view."""

    default_template_name = 'crudlfap/update.html'
