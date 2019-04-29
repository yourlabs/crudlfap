from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _


class ModelMixin(object):
    """Mixin for views using a Model class but no instance."""
    model = None

    menus = ['model']
    menus_display = ['model']
    pluralize = False

    def get_exclude(self):
        return []

    def get_fields(self):
        return [
            f for f in self.router.get_fields(self)
            if self.model._meta.get_field(f).editable
            and f not in self.exclude
        ]

    def get_model_verbose_name(self):
        if self.pluralize:
            return self.model._meta.verbose_name_plural
        else:
            return self.model._meta.verbose_name

    def get_title(self):
        """Compose a title of Model Name: View label."""
        return '{}: {}'.format(
            self.model_verbose_name.capitalize(),
            _(self.view_label),
        ).capitalize()

    def get_queryset(self):
        """Return router.get_queryset() by default, otherwise super()."""
        if self.router:
            return self.router.get_queryset(self)

        if self.model:
            return self.model._default_manager.all()

        raise ImproperlyConfigured(
            "%(cls)s is missing a QuerySet. Define "
            "%(cls)s.model, %(cls)s.queryset, or override "
            "%(cls)s.get_queryset()." % {
                'cls': self.__class__.__name__
            }
        )
