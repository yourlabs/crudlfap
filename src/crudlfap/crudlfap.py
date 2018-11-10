from crudlfap.models import Controller, URL
from crudlfap.router import Router
from crudlfap.views import generic

from django import forms
from django.contrib.auth.models import Group, Permission


class ControllerRouter(Router):
    model = Controller

    views = [
        generic.DetailView,
        generic.ListView.clone(
            search_fields=(
                'app',
                'model',
            ),
            table_fields=(
                'app',
                'model',
            ),
        ),
    ]


# useless ?
# ControllerRouter().register()


class AuthorizeView(generic.ObjectFormView):
    material_icon = 'lock'

    class form_class(forms.Form):
        groups = forms.ModelMultipleChoiceField(
            queryset=Group.objects.all(),
            required=False,
            widget=forms.CheckboxSelectMultiple,
        )

    def get_initial(self):
        kwargs = dict(
            codename=self.object.codename,
        )

        if self.object.model:
            kwargs['content_type'] = self.object.content_type

        perm = Permission.objects.filter(**kwargs).first()

        if not perm:
            return dict()

        return dict(
            groups=perm.group_set.all(),
        )

    def form_valid(self):
        perm = self.object.get_or_create_permission()
        for group in self.form.cleaned_data['groups']:
            group.permissions.add(perm)
        return super().form_valid()


class URLRouter(Router):
    model = URL
    material_icon = 'link'

    views = [
        generic.DetailView,
        AuthorizeView,
        generic.ListView.clone(
            search_fields=(
                'name',
                'controller__app',
                'controller__model',
            ),
            table_fields=(
                'controller',
                'id',
                'fullurlpath',
            ),
        ),
    ]


URLRouter().register()
