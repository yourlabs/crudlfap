from crudlfap import crudlfap

from .models import Post


class PostRouter(crudlfap.Router):
    fields = '__all__'
    icon = 'music'
    model = Post

    views = [
        crudlfap.DeleteView,
        crudlfap.UpdateView,
        crudlfap.CreateView,
        crudlfap.DetailView,
        crudlfap.FilterTables2ListView.clone(
            filter_fields=['owner'],
            search_fields=['name'],
        ),
    ]

    def allowed(self, view):
        user = view.request.user
        perms = view.required_permissions

        if perms == ['blog.add_post']:
            return user.is_authenticated

        if perms in [['blog.change_post'], ['blog.delete_post']]:
            return view.object.editable(user)

        return True

    def get_objects_for_user(self, user, perms):
        if perms in [['blog.change_post'], ['blog.delete_post']]:
            return self.model.objects.get_queryset().editable(user)
        return self.model.objects.get_queryset().readable(user)

PostRouter().register()
