from django.contrib.admin.models import CHANGE

from .modelform import ModelFormMixin
from .object import ObjectMixin


class ObjectFormMixin(ObjectMixin, ModelFormMixin):
    """Custom form view mixin on an object."""
    log_action_flag = CHANGE

    def get_success_message(self):
        return _(
            '%s %s: {}' % (_(self.view_label), self.model_verbose_name)
        ).format(self.form.instance).capitalize()

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
