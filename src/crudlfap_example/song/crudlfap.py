from crudlfap import crudlfap

from .models import Song


def authenticated(view):
    return True if view.request.user.is_authenticated else False


def owner_or_staff(view):
    return view.request.user.is_staff or view.object.owner == view.request.user


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
    model = Song

    views = [
        crudlfap.DeleteView.clone(allow=owner_or_staff),
        crudlfap.UpdateView,
        crudlfap.CreateView.clone(allow=authenticated),
        crudlfap.DetailView.clone(allow=authenticated),
        crudlfap.FilterTables2ListView.clone(
            filter_fields=['artist'],
            search_fields=['artist__name', 'name'],
        ),
    ]

SongRouter().register()
