from crudlfap import shortcuts as crudlfap

from .models import Song


class SongMixin:
    allowed_groups = 'any'

    def get_exclude(self):
        if not self.request.user.is_staff:
            return ['owner']
        return super().get_exclude()


class SongCreateView(SongMixin, crudlfap.CreateView):
    def form_valid(self):
        self.form.instance.owner = self.request.user
        return super().form_valid()


class SongRouter(crudlfap.Router):
    fields = '__all__'
    material_icon = 'album'
    model = Song

    views = [
        crudlfap.DeleteView.clone(SongMixin),
        crudlfap.UpdateView.clone(SongMixin),
        SongCreateView,
        crudlfap.DetailView.clone(
            authenticate=False,
        ),
        crudlfap.ListView.clone(
            authenticate=False,
            filter_fields=['artist'],
            search_fields=['artist__name', 'name'],
        ),
    ]

    def get_queryset(self, view):
        user = view.request.user

        if user.is_staff or user.is_superuser:
            return self.model.objects.all()
        elif not user.is_authenticated:
            return self.model.objects.none()

        return self.model.objects.filter(owner=user)


SongRouter().register()
