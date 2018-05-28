from django.contrib.admin.models import CHANGE
from django.utils.translation import ugettext as _

from .modelform import ModelFormMixin
from .object import ObjectMixin


class ObjectFormMixin(ObjectMixin, ModelFormMixin):
    """Custom form view mixin on an object."""
    log_action_flag = CHANGE

    def get_form_valid_message(self):
        return _(
            '%s %s: {}' % (_(self.view_label), self.model_verbose_name)
        ).format(self.object).capitalize()
