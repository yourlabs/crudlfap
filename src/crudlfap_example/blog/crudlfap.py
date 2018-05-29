from crudlfap import crudlfap

from .models import Post


class PostMixin:
    def get_exclude(self):
        if not self.request.user.is_staff:
            return ['owner']
        return super().get_exclude()


class PostCreateView(PostMixin, crudlfap.CreateView):
    def form_valid(self):
        self.form.instance.owner = self.request.user
        return super().form_valid()


class PostUpdateView(PostMixin, crudlfap.UpdateView):
    pass


class PostListView(crudlfap.ListView):
    def get_filter_fields(self):
        if self.request.user.is_staff:
            return ['owner']
        return []


class PostRouter(crudlfap.Router):
    fields = '__all__'
    icon = 'music'
    model = Post

    views = [
        crudlfap.DeleteObjectsView,
        crudlfap.DeleteView,
        PostUpdateView,
        PostCreateView,
        crudlfap.DetailView,
        PostListView.clone(
            search_fields=['name'],
        ),
    ]

    def allowed(self, view):
        """Example getting out of the django permission system."""
        user = view.request.user
        perms = view.required_permissions

        if perms == ['blog.add_post']:
            return user.is_authenticated
        elif perms == ['blog.change_post']:
            return view.object.editable(user)
        elif perms == ['blog.delete_post']:
            if hasattr(view, 'object'):
                return view.object.editable(user)

            # DeleteObjects relies on get_objects_for_user
            return user.is_authenticated

        return True

    def get_objects_for_user(self, user, perms):
        if perms in [['blog.change_post'], ['blog.delete_post']]:
            return self.model.objects.get_queryset().editable(user)
        elif perms in [['blog.list_post'], ['blog.detail_post']]:
            return self.model.objects.get_queryset().readable(user)
        else:
            return self.model.objects.get_queryset().none()

PostRouter().register()
