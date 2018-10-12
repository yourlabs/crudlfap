"""Extending CRUDLFAP features."""

from crudlfap import crudlfap
from .models import Post


crudlfap.Router(
    Post,
    views=[]
).register()


class PostMixin:
    """Create mixin."""
    def get_exclude(self):
        if not self.request.user.is_staff:
            return ['owner']
        return super().get_exclude()


class PostCreateView(PostMixin, crudlfap.CreateView):
    """Override Post create view."""
    def form_valid(self):
        """Assigned currnet user."""
        self.form.instance.owner = self.request.user
        return super().form_valid()


crudlfap.Router(
    Post,
    material_icon='forum',
    namespace='posts',
    views=[
        crudlfap.ListView.clone(
            filter_fields=['owner'],
            search_fields=['name', 'publish', 'owner'],
        ),
        PostCreateView,
        crudlfap.UpdateView,
        crudlfap.DeleteView,
    ]
).register()
