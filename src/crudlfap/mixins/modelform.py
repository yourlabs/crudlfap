from .form import FormMixin
from .model import ModelMixin


class ModelFormMixin(ModelMixin, FormMixin):
    """ModelForm Mixin using readable"""
    log_action_flag = False
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

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request,
            self.message_html(self.form_invalid_message)
        )
        return response

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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            self.message_html(self.form_valid_message)
        )
        self.log_insert()
        return response
