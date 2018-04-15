from crudlfap import crudlfap

from .models import Song


class SongRouter(crudlfap.Router):
    fields = '__all__'
    icon = 'music'
    model = Song

    views = [
        crudlfap.DeleteView,
        crudlfap.UpdateView,
        crudlfap.CreateView,
        crudlfap.DetailView,
        crudlfap.FilterTables2ListView.clone(
            filter_fields=['artist'],
            search_fields=['artist__name', 'name'],
        ),
    ]

    def allowed(self, view):
        # In this example, we let users do everything on their own objects
        # and that's taken care of by get_objects_for_user. So, we short-
        # circuit the Django permission system which takes place by default
        # We only have the create view that does not go through
        # get_objects_for_user, deal with that
        return view.request.user.is_authenticated

    def get_objects_for_user(self, user, perms):
        if not user.is_authenticated:
            return self.model.objects.none()

        if user.is_staff or user.is_superuser:
            return self.model.objects.all()

        return self.model.objects.filter(owner=user)

SongRouter().register()
