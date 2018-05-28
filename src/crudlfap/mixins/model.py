from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _


class ModelMixin(object):
    """Mixin for views using a Model class but no instance."""
    model = None

    menus = ['model']
    menus_display = ['model']
    pluralize = False
    object_permission_check = False

    def get_exclude(self):
        return []

    def get_fields(self):
        return [
            f for f in self.router.get_fields_for_user(
                self.request.user,
                self.required_permissions
            )
            if self.model._meta.get_field(f).editable
            and f not in self.exclude
        ]

    def get_model_verbose_name(self):
        if self.pluralize:
            return self.model._meta.verbose_name_plural
        else:
            return self.model._meta.verbose_name

    def get_title(self):
        return '{}: {}'.format(
            self.model_verbose_name.capitalize(),
            _(self.view_label),
        ).capitalize()

    def get_queryset(self):
        """Return router.get_queryset() by default, otherwise super()."""
        if self.router:
            qs = self.router.get_objects_for_user(
                self.request.user,
                self.required_permissions,
            )
        else:
            if self.model:
                qs = self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )

        return qs
