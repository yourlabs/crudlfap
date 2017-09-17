Welcome to CRUDLFA+ for Django 2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CRUDLFA+ stands for Create Read Update Delete List Form Autocomplete and more.

This package provides a more DRY way to rapidely develop modern web
applications by thinking differently:

- Composition over inheritance with an intermediary layer to use in urls.py,
- JavaScript is a first class citizen,
- Integration with external Django apps more than welcome.

Examples
========

You want a modern CRUD for your Server model where you can override default
templates::

    from crudlfap import shortcuts as crudlfap
    from .models import Server

    urlpatterns = crudlfap.ModelViewRouter(Server).urlpatterns()

Don't forget to open the debug url as superuser, to see the list of url
patterns and names and views and menus etc and everything it did for you
because crudlfap+ loves you.

Let's setup some permissions OOAO::

    class ServerRouter(ModelViewRouter):
        # used by anything from autocomplete view to related forms fields:
        def get_queryset(self, request):
            if not request.user.is_authenticated():
                return None

            if not request.user.is_staff:
                return Server.objects.filter(
                    Q(public=True)|Q(owner=request.user)
                )

            return Server.objects.all()

        # used by anything from generating menus to actual security
        def allow(self, user, view, model=None):
            return user.is_authenticated() and view.allow(user, model)

    urlpatterns = ServerRouter(Server).urlpatterns()


You want to override a view and call some custom code ie. from your model
manager::

    class ServerCreateView(crudlfap.CreateView):
        title = _('Deploy a new Server')

        def form_valid(self, form):
            # Example custom code:
            Server.objects.deploy(form.cleaned_data['name'])
            return super().form_valid(form)

    class ServerRouter(crudlfap.ModelViewRouter):
        # Permission code from above not re-pasted here
        views = crudlfap.ModelViewRouter.views + [ServerCreate]
    urlpatterns = ServerRouter(Server).urlpatterns()


You want to add another view on a model instance such as to refresh a server::

    from django import forms
    from django.contrib import messages

    class ServerRefreshView(crudlfap.FormView):
        menus = ['object_actions']  # show in detail and list view
        icon = 'fa fa-refresh'  # icon for this view / menu links
        style = 'warning'  # view style variable

        def allow(self, user, model=None):
            # if we wanted to also limit edit/delete to the same rule, we'd
            # move this in ServerRouter.allow. Having this code here only
            # protects this view class.
            return model.is_public or model.owner == user

        def form_valid(self, form):
            try:
                self.object.refresh_from_your_cloud()
            except YourCloudException as e:
                if self.request.user.
                messages.error(_('Server {} refresh fail').format(self.object))
            else:
                messages.success(_('Server {} refreshed').format(self.object))
            return self.object.get_absolute_url


    class ServerRouter(crudlfap.ModelViewRouter):
        views = crudlfap.ModelViewRouter.views + [
            ServerCreateView, ServerRefreshView]
    urlpatterns = ServerRouter(Server).urlpatterns()
