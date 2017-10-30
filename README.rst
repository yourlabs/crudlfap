Welcome to CRUDLFA+ for Django 2.0: because Django is FUN !
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CRUDLFA+ stands for Create Read Update Delete List Form Autocomplete and more.

This package provides a more DRY way to rapidely develop modern web
applications by thinking differently:

- Composition over inheritance with an intermediary layer to use in urls.py,
- JavaScript is a first class citizen,
- Integration with external Django apps more than welcome,

Consider this as a brand new framework with a lot of modern features, except
you don't have to learn a new framework because this is still Django, with a
2017 feels: https://www.youtube.com/watch?v=lGqeXp6zeo8

Try
===

This should start the example project in ``src/crudlfap_example`` where each
documented example lives::

    # Clean virtual env
    rm -rf /tmp/crudlfap_env ; virtualenv /tmp/crudlfap_env ; source /tmp/crudlfap_env/bin/activate
    # Stable
    pip install crudlfap[django,tables2,filter,dal,reversion,debug]; crudlfap dev
    # or Development
    pip install -e git+https://github.com/yourlabs/crudlfap.git#egg=crudlfap[django,tables2,filter,dal,reversion,debug]; crudlfap dev

Features
========

- Modern url router,
- Ajax routing framework,
- Ajax / modal forms (ie. ajax file upload with progressbar),
- Default templates for CRUD with Propeller CSS framework (provides Material
  design for bootstrap3's HTML and select2.js !)

Install
=======

To add crudlfap to your project, first copy over settings from
``crudlfap_example.settings.TEMPLATES`` or enable jinja2 manually. Also set
``LOGIN_REDIRECT_URL = '/'`` for now.

Then add ``crudlfap`` to your ``settings.INSTALLED_APPS``. You can find other
crudlfap apps you can add with the following commmand::

    echo 'from django.conf import settings; settings.INSTALLED_APPS' | crudlfap shell | grep crud

You will also need a context processor that sets the ``base`` template
context, ie. ``crudlfap.context_processors.base``, but then again, just copy
over the ``TEMPLATES`` .

Examples
========

Let's hack a modern CRUD for your Server model where you can override default
templates, add this to your app's ``urls.py``:

.. code-block:: python

    from crudlfap import crudlfap
    from .models import Server

    urlpatterns = crudlfap.Router(
        Server,
        fields='__all__',
        menus=['main'],
        allow=lambda view, user: return True, # Default requires is_staff!
    ).urlpatterns()

Then, add it to your project's ``urls.py``:

.. code-block:: python

    urlpatterns = [
    
        url(r'^yourapp/', include('yourapp.urls')),  # what you created above
        url(r'^crudlfap/', include('crudlfap.urls')),  # for debug views
        
        # for auth views, we haz material templates
        url(r'^auth/', include('django.contrib.auth.urls')),
        url(r'^$', generic.TemplateView.as_view(template_name='crudlfap/home.html')),  # for free

        # Also, remove django.contrib.admin from ehere and INSTALLED_APPS, not
        # that it's not compatible, but CRUDLFA+ provides better features so do
        # yourself a favor in 2017 and use CRUDLFA+'s modern router instead
    ]

Now, open your browser and learn to love CRUDFA+ and look at your material
design website. Don't forget to check the registered url list which was
generated for you.

Let's setup the default queryset per user for views and forms etc and set
some permissions on views and fields, all OOAO:

.. code-block:: python


    def authenticated(view, user):
        return True if user.is_authenticated() else False


    def owner_or_staff(view, user):
        return user.is_staff or view.object.owner == user


    class ServerUpdateView(ServerOwnerRequired, crudlfap.UpdateView):
        allow = owner_or_staff

        def get_fields(self):
            if request.user.is_staff:
                return ['name', 'owner']
            else:
                return ['name']


    class ServerRouter(Router):
        menus = ['main']  # Yes Django can make menus from your URL definition
        material_icon = 'server'  # Yes with icons

        views = [
            ServerCreateView.factory(allow=authenticated),
            crudlfap.DetailView.factory(fields=['name', 'owner', 'created']),
            'crudlfap.views.generic.ListView',
            ServerUpdateView.factory(allow=owner_or_staff),
            ServerDeleteView.factory(allow=owner_or_staff),
        ]

        # yes django allows OOAO for viewland, and you can invent words too
        def get_queryset(self, user):
            if not user.pk:
                return Server.objects.filter(is_public=True)

            if not request.user.is_staff:
                return self.model.objects.filter(
                    Q(is_public=True)|Q(owner=request.user)
                )

            return self.model.objects.all()
    urlpatterns = ServerRouter(Server).urlpatterns()

Example generating a menu which rocks in 2017::

    {% for v in Router.registry[object].get_menu('object') %}
      {% set v=v.factory(object=object)() %}
      {% if v != view and view.allow(request.user) %}
        {#
        above we check that it's not the same as the current
        view and that the user has permission too
        #}
        <a
          href="{{ view.reverse(object) }}"
          target="{{ view.target }}"
          data-ajax="{{ view.ajax }}"
          title="{{ view.get_title() }}" # hell yes, soooooo 2017 !!! let's DRY !
          ><i class="material-icon material-{{ view.material_icon }}"></i></a>
      {% endif %}
    {% endif %}

Example checking security in Python::

    if crudlfap.Router.registry[obj]['update'].factory(object=obj).allow(user):
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
custom actions on this model:

.. code-block:: python

    from django import forms
    from django.contrib import messages

    class ServerRefreshView(crudlfap.FormView):
        menus = ['object_actions']  # show in detail and list view
        fa_icon = 'refresh'  # icon for this view / menu links
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
dear knock yourself out:

.. code-block:: python

    class ServerRouter(crudlfap.Router):
        views = [
            'yourapp.views.ServerCreateView',
            crudlfap.DetailView.factory(fields=['name']),
            crudlfap.import_string(
                'crudlfap_filtertables2.views.FilterTables2ListView'
            ).factory(
                filter_fields=['location', 'name'],
            ),
            'crudlfap.ReversionView',
            'yourapp.views.ServerUpdateView',
            ServerDeleteView,
            ServerRefreshView,
        ]
    urlpatterns = ServerRouter(Server).urlpatterns()
