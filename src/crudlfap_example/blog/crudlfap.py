from crudlfap import shortcuts as crudlfap

from .models import Post


class AuthBackend:
    def authenticate(self, *args):
        return None  # prevent auth from this backend

    def has_perm(self, user_obj, perm, obj=None):
        view = obj

        if view.model != Post:
            return False

        user = user_obj
        code = view.permission_shortcode

        if code in ('list', 'detail'):
            return True
        elif code == 'add':
            return user.is_authenticated
        elif code == 'change':
            return view.object.editable(user)
        elif code == 'delete':
            if hasattr(view, 'object'):
                return view.object.editable(user)

            # DeleteObjects relies on get_queryset to secure runtime
            return user.is_authenticated

        return super().has_perm(user_obj, perm, obj)


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

    def get_queryset(self, view):
        qs = self.model.objects.get_queryset()
        if view.request.user.is_superuser:
            return qs
        elif view.permission_shortcode in ('change', 'delete'):
            return qs.editable(view.request.user)
        elif view.permission_shortcode in ('list', 'detail'):
            return qs.readable(view.request.user)
        return qs.none()


PostRouter().register()
