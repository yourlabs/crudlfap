from crudlfap import crudlfap

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group
from django.urls import path

from . import views


User = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))


def superuser(view):
    return view.request.user.is_superuser


urlpatterns = crudlfap.Router(
    User,
    views=[
        crudlfap.DeleteView,
        crudlfap.UpdateView,
        crudlfap.CreateView,
        crudlfap.DetailView,
        views.PasswordView,
        views.BecomeUser,
        crudlfap.FilterTables2ListView.factory(
            search_fields=['username', 'email', 'first_name', 'last_name'],
            table_fields=['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser'],
            filter_fields=['groups', 'is_superuser', 'is_staff'],
        ),
    ],
    allow=lambda view: view.request.user.is_superuser,
    url_field='username',
    url_prefix='user',
).urlpatterns() + crudlfap.Router(
    Group,
    url_field='name',
    url_prefix='group',
).urlpatterns() + [
    path('su', views.Become.as_view(model=User), name='user_become'),
]
