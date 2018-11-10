from crudlfap import shortcuts as crudlfap

from .models import Song


class SongMixin:
    def get_exclude(self):
        if not self.request.user.is_staff:
            return ['owner']
        return super().get_exclude()


class SongCreateView(SongMixin, crudlfap.CreateView):
    def form_valid(self):
        self.form.instance.owner = self.request.user
        return super().form_valid()


class SongUpdateView(SongMixin, crudlfap.UpdateView):
    pass


class SongRouter(crudlfap.Router):
    fields = '__all__'
    icon = 'music'
    model = Song

    views = [
        crudlfap.DeleteView,
        SongUpdateView,
        SongCreateView,
        crudlfap.DetailView,
        crudlfap.ListView.clone(
            filter_fields=['artist'],
            search_fields=['artist__name', 'name'],
        ),
    ]

    def get_queryset(self, view):
        user = view.request.user
        if not user.is_authenticated:
            return self.model.objects.none()

        if user.is_staff or user.is_superuser:
            return self.model.objects.all()

        return self.model.objects.filter(owner=user)


SongRouter().register()
