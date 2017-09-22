from crudlfap import crudlfap

from django.apps import apps
from django.conf import settings


User = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))


def superuser(view, user):
    return user.is_superuser


urlpatterns = crudlfap.Router(
    User,
    crudlfap.DeleteView,
    crudlfap.UpdateView,
    crudlfap.DetailView,
    crudlfap.CreateView,
    crudlfap.ListView.factory(slug_url_kwarg='username'),
    allow=lambda view, user: user.is_superuser,
).urlpatterns()
