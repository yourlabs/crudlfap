Welcome to CRUDLFA+ for Django 2.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CRUDLFA+ stands for Create Read Update Delete List Form Autocomplete and more.

This package provides a more DRY way to rapidely develop modern web
applications by thinking differently:

- Composition over inheritance with an intermediary layer to use in urls.py,
- JavaScript is a first class citizen,
- Integration with external Django apps more than welcome,

Try
===

This should start the example project in ``src/crudlfap_example`` where each
documented example lives::

    pip install --user crudlflap[django][tables2][filter][dal]; crudlfap runserver

Examples
========

Let's hack a modern CRUD for your Server model where you can override default
templates::

    from crudlfap import shortcuts as crudlfap
    from .models import Server

    # Use fields='__all__' to allow read/write on all model fields for
    # everybody for now
    urlpatterns = crudlfap.Router(Server, fields='__all__').urlpatterns()

Now, open your browser and learn to love CRUDFA+ and stop worrying. Don't
forget to open the debug url as superuser, to see the list of url patterns and
names and views and menus etc and everything it did for you because crudlfap+
loves you.

Let's setup the default queryset per user for views and forms etc and set
some permissions on views and fields, all OOAO::


    class ServerCreateView(crudlfap.CreateView):
        @classmethod
        def allow(cls, user):
            return True if user.is_authenticated() else False


    class ServerFormViewMixin(crudlfap.FormViewMixin):
        @classmethod
        def allow(cls, user, model):
            return user.is_staff or model.owner == user


    class ServerUpdateView(ServerFormViewMixin, crudlfap.CreateView):
        pass


    class ServerDeleteView(ServerFormViewMixin, crudlfap.CreateView):
        pass


    class ServerRouter(Router):
        views = [
            ServerCreateView,
            crudlfap.DetailView,
            crudlfap.ListView,
            ServerUpdateView,
            ServerDeleteView,
        ]

        readable_fields = ['name', 'owner', 'created']

        def get_writable_fields(self, user):
            if request.user.is_staff:
                return ['name', 'owner']
            else:
                return ['name']

        # used by anything from autocomplete view to related forms fields
        def get_queryset(self, user):
            if not user.pk:
                return Server.objects.filter(is_public=True)

            if not request.user.is_staff:
                return self.model.objects.filter(
                    Q(is_public=True)|Q(owner=request.user)
                )

            return self.model.objects.all()
    urlpatterns = ServerRouter(Server).urlpatterns()

Example checking security in template (Jinja2)::

    {% if crulfap_router(object).get_view_by_slug('update').allow(request.user, object) %}

Example checking security in Python::

    if crudlfap.routers['yourapp.server']['update'].allow(user, server):
        # User has permission to update on the default router for yourapp.Server

Now if you want to make your own link to an object update modal because you are
in 2017 then you could use this Jinja2 function::

    {% cruldfap_modal object 'update' %}

Note that the above won't render anything if the user doesn't have the
permission to execute the update view.

Now if you want to render a particular model field attribute after checking
user permission::

    {% if 'created' in crudlfap_router(object).get_writable_fields(request.user) %}
        {% crudlfap_attribute_label object 'created' %}: {% crudlfap_attribute_value object 'created' %}
    {% endif %}

Or just::

    {% crudlfap_attribute object 'created' %}

Check the default templates for moar 2017 DRY fun !

Now, if you think this pattern is too 2017 for you, wait until we add some
custom actions on this model::

    from django import forms
    from django.contrib import messages

    class ServerRefreshView(crudlfap.FormView):
        menus = ['object_actions']  # show in detail and list view
        icon = 'fa fa-refresh'  # icon for this view / menu links
        style = 'warning'  # view style variable

        def allow(self, user, model=None):
            return model.is_public or model.owner == user

        def form_valid(self, form):
            try:
                self.object.refresh_from_your_cloud()
            except YourCloudException as e:
                if self.request.user.is_staff:
                    messages.error(unicode(e))
                else:
                    messages.error(_('Server {} refresh fail').format(self.object))
                logger.exception('Failed to refresh server')
            else:
                messages.success(_('Server {} refreshed').format(self.object))
            return self.object.get_absolute_url()


    class ServerRouter(crudlfap.Router):
        views = [
            ServerCreateView,
            crudlfap.DetailView,
            crudlfap.ListView,
            ServerUpdateView,
            ServerDeleteView,
            ServerRefreshView,
        ]
    urlpatterns = ServerRouter(Server).urlpatterns()

Refresh your browser and you will see a new "refresh" button with the
'fa-refresh' icon in the list view and the detail view

Ok so you want to integrate django-reversion and django-tables2 then please
dear knock yourself out::

    class ServerRouter(crudlfap.Router):
        views = [
            ServerCreateView,
            crudlfap.DetailView,
            crudlfap.Tables2ListView,
            crudlfap.ReversionView,
            ServerUpdateView,
            ServerDeleteView,
            ServerRefreshView,
        ]
    urlpatterns = ServerRouter(Server).urlpatterns()
