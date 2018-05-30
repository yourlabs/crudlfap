from django.utils.translation import ugettext as _

from .modelform import ModelFormMixin


class ObjectsFormMixin(ModelFormMixin):
    pluralize = True
    link_attributes = {
        'data-listaction': 'urlupdate',
    }
    menus = ['list_action']

    def get_invalid_pks(self):
        return len(self.request.GET.getlist('pks')) - len(self.object_list)

    def get_object_list(self):
        self.object_list = self.queryset.filter(
            pk__in=self.request.GET.getlist('pks')
        )
        return self.object_list

    def get_success_url(self):
        return self.router['list'].reverse()

    def get_form_valid_message(self):
        return '{}: {}'.format(
            _(self.view_label),
            ', '.join([str(o) for o in self.object_list]),
        ).capitalize()
