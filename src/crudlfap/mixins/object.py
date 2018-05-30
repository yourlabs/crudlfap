from django import http
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .model import ModelMixin


class ObjectMixin(ModelMixin):
    """Mixin for views using a Model instance."""

    menus = ['object', 'object_detail']
    menus_display = ['object', 'object_detail']
    object_permission_check = True
    template_name_field = None

    def get_context(self, **context):
        context['object'] = self.object
        return super().get_context(**context)

    def get_template_name_suffix(self):
        return '_{}'.format(self.urlname)

    def get_urlargs(self):
        """Return list with object's urlfield attribute."""
        return [getattr(self.object, self.urlfield)]

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
        return '{} "{}": {}'.format(
            self.model_verbose_name,
            self.object,
            _(self.view_label).capitalize(),
        ).capitalize()

    def get_menu_kwargs(self):
        return dict(object=self.object)

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        if getattr(self, 'kwargs', False) is False:
            # This happens when the view has not been instanciated with an
            # object, neither from a URL which would allow getting the object
            # in the super() call below.
            raise Exception('Must instanciate the view with an object')

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        queryset = queryset.filter(
            **{self.urlfield: self.kwargs.get(self.urlfield)}
        )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise http.Http404(
                _("No %(verbose_name)s found matching the query") %
                {'verbose_name': queryset.model._meta.verbose_name}
            )

        return obj

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

    def get_template_names(self):
        """
        Return a list of template names to be used for the request.

        May not be called if render_to_response() is overridden. Return the
        following list:

        * the value of ``template_name`` on the view (if provided)
        * the contents of the ``template_name_field`` field on the
          object instance that the view is operating upon (if available)
        * ``<app_label>/<model_name><template_name_suffix>.html``
        """
        try:
            names = super().get_template_names()
        except (ImproperlyConfigured, AttributeError):
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

            # If self.template_name_field is set, grab the value of the field
            # of that name from the object; this is the most specific template
            # name, if given.
            if self.object and self.template_name_field:
                name = getattr(self.object, self.template_name_field, None)
                if name:
                    names.insert(0, name)

            # The least-specific option is the default
            # <app>/<model>_detail.html; only use this if the object in
            # question is a model.
            if isinstance(self.object, models.Model):
                object_meta = self.object._meta
                names.append("%s/%s%s.html" % (
                    object_meta.app_label,
                    object_meta.model_name,
                    self.template_name_suffix
                ))
            elif self.model and issubclass(self.model, models.Model):
                names.append("%s/%s%s.html" % (
                    self.model._meta.app_label,
                    self.model._meta.model_name,
                    self.template_name_suffix
                ))

            # If we still haven't managed to find any template names, we should
            # re-raise the ImproperlyConfigured to alert the user.
            if not names:
                raise

        return names
