from crudlfap import crudlfap

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import path

from . import views


User = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))


def superuser(view):
    return view.request.user.is_superuser


crudlfap.Router(
    User,
    views=[
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
            fields=['username', 'email', 'groups', 'is_staff', 'is_superuser']
        ),
        views.PasswordView,
        views.BecomeUser,
        crudlfap.DetailView.clone(exclude=['password']),
        crudlfap.FilterTables2ListView.clone(
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
    allow=lambda view: view.request.user.is_superuser,
    urlfield='username',
    material_icon='person',
).register()

crudlfap.Router(
    Group,
    fields=['name', 'permissions'],
    urlfield='name',
    material_icon='group',
).register()

crudlfap.site.views.append(views.Become.clone(model=User))
