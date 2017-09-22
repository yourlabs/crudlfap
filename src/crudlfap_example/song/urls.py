from crudlfap import crudlfap

from .models import Song


def authenticated(view, user):
    return True if user.is_authenticated() else False


def owner_or_staff(view, user):
    return user.is_staff or view.object.owner == user


class SongUpdateView(crudlfap.UpdateView):
    allow = owner_or_staff

    def get_fields(self):
        if self.request.user.is_staff:
            return ['name', 'owner']
        else:
            return ['name']


class SongRouter(crudlfap.Router):
    fields = '__all__'
    icon = 'music'

    views = [
        crudlfap.DeleteView.factory(allow=owner_or_staff),
        crudlfap.UpdateView,
        crudlfap.DetailView.factory(allow=authenticated),
        crudlfap.CreateView.factory(allow=authenticated),
        crudlfap.FilterTables2ListView.factory(
            filter_fields=['artist', 'name'],
        ),
    ]

urlpatterns = SongRouter(Song).urlpatterns()
