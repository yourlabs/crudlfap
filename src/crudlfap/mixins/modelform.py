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
        if hasattr(self, 'object'):
            self.form_kwargs.update({'instance': self.object})
        return self.form_kwargs

    def get_form(self):
        self.form = self.form_class(**self.form_kwargs)

    def get_form_fields(self):
        if hasattr(self.router, 'form_fields'):
            return self.router.form_fields
        if hasattr(self.router, 'fields'):
            return self.router.fields
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
        if self.form.instance:
            try:
                url = self.form.instance.get_absolute_url()
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

        LogEntry.objects.log_action(
            self.request.user.pk,
            ContentType.objects.get_for_model(self.model).pk,
            self.object.pk,
            str(self.object),
            self.log_action_flag,
            self.log_message,
        )

    def form_valid(self):
        self.object = self.form.save()
        self.log_insert()
        return super().form_valid()
