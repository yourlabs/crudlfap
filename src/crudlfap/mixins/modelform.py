from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.forms import models as model_forms
from django.utils.translation import ugettext as _

from .form import FormMixin
from .model import ModelMixin


class ModelFormMixin(ModelMixin, FormMixin):
    """ModelForm Mixin using readable"""
    menus = ['model']

    def get_form_kwargs(self):
        self.form_kwargs = super().get_form_kwargs()
        if (hasattr(self, 'object')
                and issubclass(self.form_class, model_forms.ModelForm)):

            self.form_kwargs.update({'instance': self.object})
        return self.form_kwargs

    def get_form(self):
        self.form = self.form_class(**self.form_kwargs)

    def get_form_fields(self):
        return self.fields

    def get_form_class(self):
        return model_forms.modelform_factory(
            self.model,
            fields=self.form_fields
        )

    def get_form_invalid_message(self):
        return '{}: {}: {}'.format(
            _(self.view_label),
            self.model_verbose_name,
            _('failure'),
        ).capitalize()

    def get_form_valid_message(self):
        return '{}: {}'.format(
            _(self.view_label),
            self.form.instance,
        ).capitalize()

    def message_html(self, message):
        """Add the detail url for form.instance, if possible."""
        if getattr(self, 'object', None):
            try:
                url = self.object.get_absolute_url()
            except:
                return message

            return ' '.join((
                message,
                '<a href="{}" class="btn-flat toast-action">{}</a>'.format(
                    url,
                    _('detail').capitalize(),
                ),
            ))
        return message

    def get_log_action_flag(self):
        return False

    def get_log_message(self):
        return _(self.view_label)

    def log_insert(self):
        if not LogEntry:
            return

        if not self.request.user.is_authenticated:
            return

        if not self.log_action_flag:
            return

        if hasattr(self, 'object_list'):
            objects = self.object_list
        else:
            objects = [self.object]

        for obj in objects:
            LogEntry.objects.log_action(
                self.request.user.pk,
                ContentType.objects.get_for_model(self.model).pk,
                obj.pk,
                str(obj),
                self.log_action_flag,
                self.log_message,
            )

    def form_valid(self):
        response = super().form_valid()
        self.log_insert()
        return response
