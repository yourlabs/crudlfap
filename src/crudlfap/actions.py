from crudlfap.factory import Factory
from crudlfap.views.list import BaseListView
from crudlfap.views.generic import ModelFormView, ObjectFormView

from django import forms
from django.contrib import messages
from django.contrib.admin.models import DELETION


class Action(Factory):
    controller = 'modal'
    action = 'click->modal#open'
    form_class = forms.Form


    object_menus = ['object', 'object_detail']
    objects_menus = ['list_action']

    def get_object_view(self):
        view = type(
            self.cls.__name__.replace('Action', 'View'),
            (self.cls, ObjectFormView),
            dict(
                menus=self.object_menus,
            )
        )
        return view

    def get_objects_view(self):
        view = type(
            self.cls.__name__.replace('Action', 'SelectedView'),
            (self.cls, ModelFormView, BaseListView),
            dict(
                menus=self.objects_menus,
                link_attributes={
                    'data-listaction': 'urlupdate',
                }
            )
        )
        return view


class DeleteAction(Action):
    """View to delete a model object."""

    default_template_name = 'crudlfap/delete.html'
    style = 'danger'
    fa_icon = 'trash'
    material_icon = 'delete'
    success_url_next = True
    color = 'red'
    log_action_flag = DELETION

    def get_success_message(self):
        return _(
            '%s %s: {}' % (_(self.view_label), self.model_verbose_name)
        ).format(self.object).capitalize()

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return self.router['list'].reverse()

    def get_required_permissions(self):
        return ['{}.delete_{}'.format(
            self.app_name, self.model._meta.model_name)]
