from crudlfap import crudlfap

from .models import Song


class SongRouter(crudlfap.Router):
    fields = '__all__'
    icon = 'music'

    views = [
        'crudlfap.views.generic.DeleteView',
        'crudlfap.views.generic.UpdateView',
        'crudlfap.views.generic.DetailView',
        'crudlfap.views.generic.CreateView',
        dict(
            _cls='crudlfap_filtertables2.views.FilterTables2ListView',
            filter_fields=['artist', 'name'],
        )
    ]

urlpatterns = SongRouter(Song).urlpatterns()
