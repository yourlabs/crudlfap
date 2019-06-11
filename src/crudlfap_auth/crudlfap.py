from crudlfap import shortcuts as crudlfap

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group

from . import views


User = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))


crudlfap.Router(
    User,
    views=[
        crudlfap.DeleteObjectsView,
        crudlfap.DeleteView,
        crudlfap.UpdateView.clone(
            fields=[
                'username',
                'email',
                'first_name',
                'last_name',
                'groups',
                'is_superuser',
                'is_staff',
                'is_active',
            ]
        ),
        crudlfap.CreateView.clone(
            fields=[
                'username',
                'email',
                'groups',
                'is_staff',
                'is_superuser'
            ],
        ),
        views.PasswordView,
        views.BecomeUser,
        crudlfap.DetailView.clone(exclude=['password']),
        crudlfap.ListView.clone(
            search_fields=[
                'username',
                'email',
                'first_name',
                'last_name'
            ],
            table_fields=[
                'username',
                'email',
                'first_name',
                'last_name',
                'is_staff',
                'is_superuser'
            ],
            filter_fields=[
                'groups',
                'is_superuser',
                'is_staff'
            ],
        ),
    ],
    urlfield='username',
    material_icon='person',
).register()


class GroupUpdateView(crudlfap.UpdateView):
    def get_form_class(self):
        cls = super().get_form_class()
        cls.base_fields['permissions'].queryset = (
            cls.base_fields['permissions'].queryset.select_related(
                'content_type'))
        return cls


crudlfap.Router(
    Group,
    fields=['name', 'permissions'],
    material_icon='group',
    views=[
        crudlfap.DeleteObjectsView,
        crudlfap.DeleteView,
        GroupUpdateView,
        crudlfap.CreateView,
        crudlfap.DetailView,
        crudlfap.ListView,
    ],
).register()

crudlfap.site.views.append(views.Become.clone(model=User))
