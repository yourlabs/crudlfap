"""
The CRUDLFA+ Router is able to generate menus checking perms, generate urls ...

.. note:: Note that you can also use non-database backed models, by inheriting
          from models.Model and setting their Meta.managed attribute to False.
          Then, you can use CRUDLFA+ views and routers.

Menus
-----

A menu is referenced by a short name, and CRUDLFA+ generic views already define
a bunch of them, but you can add your own too:

- ``object``: means the view is for a model instance,
- ``object_detail``: means the view should only be visible from detail view,
- ``model``: means the view applies to a model class, such as list view,
- ``main``: means the view should be in the main menu.

To get the views of a router, for a menu, kwargs such as the object, and with
permissions on request.user use :py:class:`Router.get_menu()`. In Jinja2
templates you can call them with:

.. code-block:: django

    {% set views=view.router.get_menu(
        'object',
        view.request,
        object=view.object
    ) %}

Now that Django can generate a menu after serious the refactoring that brought
us to discover this pattern with Etienne Vidal @ DevNix, we rely on Jinja2 to
refactor the HTML to render those menus.

The menu macro takes a list of views as argument, and also a
unique HTML id it can use to generate the dropdown.

.. code-block:: django

    {% import 'crudlfap.html' as crudlfap %}
    {{ crudlfap.dropdown(views, 'row-actions-' + str(object.pk)) }}
    {# also works, different style: #}
    {{ crudlfap.dropdownbutton(views, 'row-actions-' + str(object.pk)) }}

The above code will generate a Material design dropdown menu with an icon and
the other one as a button with all nice icons, titles, permissions checked, and
so on.  This is used everywhere you see a part of the page that can spawn to a
dropdown. If there is only one matching view, it will display only the button.
"""
from django.apps import apps
from django.conf import settings
from django.urls import path
from django.utils.module_loading import import_string

from .route import Route
from .settings import CRUDLFAP_VIEWS
from .utils import guess_urlfield


crudlfap = apps.get_app_config('crudlfap')  # pylint: disable=invalid-name


class ViewsDescriptor(object):
    def __init__(self, default=None):
        self.default = default or []

    def __get__(self, obj, objtype):
        if getattr(obj, '_views', None) is None:
            if callable(self.default):
                obj.views = self.default()
            else:
                obj.views = self.default
        return obj._views

    def __set__(self, obj, value):
        obj._views = Views(value)


class Views(list):
    def __getitem__(self, key):
        if isinstance(key, int):
            return super().__getitem__(key)

        for view in self:
            if view.urlname == key:
                return view

    def __setitem__(self, key, value):
        if isinstance(key, int):
            return super().__setitem__(key, value)

        for i, view in enumerate(self):
            if view.urlname == key:
                return super().__setitem__(i, value)

    def __delitem__(self, key):
        if isinstance(key, int):
            return super().__delitem__(key)

        for i, view in enumerate(self):
            if view.urlname == key:
                return super().__delitem__(i)


class Router(object):
    """
    Base router for CRUDLFA+ Route.

    .. py:attribute:: model

        Optional model class for this Router and all its views.
    """
    views = ViewsDescriptor(
        getattr(settings, 'CRUDFLAP_VIEWS', CRUDLFAP_VIEWS)
    )

    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}()'.format(attr[4:], attr))

        if hasattr(self, 'get_' + attr):
            return getattr(self, 'get_' + attr)()

        raise AttributeError('{} or get_{}()'.format(attr, attr))

    def get_urlfield(self):
        """
        Return Field name of model for reversing url.

        This will return model ` slug ` field if available or ` pk ` field.

        See ``guess_urlfield()`` for detail.
        """
        return guess_urlfield(self.model)

    def get_namespace(self):
        """Generate namespace for this Router views."""
        if self.model:
            return self.model._meta.model_name

    def get_urlpath(self):
        """Return Model name for urlpath."""
        if self.model:
            return self.model._meta.model_name

    def get_app_name(self):
        """Generate app name for this Router views."""
        return self.model._meta.app_label

    def get_registry(self):
        from crudlfap.crudlfap import site
        return site

    def __getitem__(self, urlname):
        """Get a view by urlname."""
        for view in self.views:
            if view.urlname == urlname:
                return view

        raise KeyError(
            'View with urlname {} not in router {}'.format(
                urlname,
                type(self).__name__,
            )
        )

    def generate_views(self, *views):
        """
        Generate views for this router, core of the automation in CRUDLFA+.

        This method considers each view in given args or self.views and returns
        a list of usable views.

        Each arg may be a view class or a dict of attributes with a `_cls` key
        for the actual view class.

        It will copy the view class and bind the router on it in the list this
        returns.

        For example, this would cause two view classes to be returned, if
        self.model is ``Artist``, then ``CreateView`` will be used as parent to
        create ``ArtistCreateView`` and ``DetailView`` will be used to create
        ``ArtistDetailView``, also setting the attribute
        ``extra_stuff='bar'``::

            Router(Artist).generate_views([
                CreateView,
                dict(_cls=DetailView, extra_stuff='bar'),
                ListView.factory(paginate_by=12),
            ])
        """
        kwargs = dict(model=self.model, router=self)
        result = []
        for action in getattr(self, 'actions', []):
            result.append(action.objects_view.clone(**kwargs))
            result.append(action.object_view.clone(**kwargs))

        for arg in views or self.views:
            view = arg

            if isinstance(view, str):
                view = import_string(view)

            try:
                if not issubclass(view, Route) and view != Route:
                    view = type(view.__name__, (view, Route), {})
            except Exception as e:
                print('Got an error with view:', view)
                raise e

            view = view.clone(**kwargs)

            result.append(view)
        return result

    def __init__(self, model=None, registry=None, views=None, **attributes):
        """Create a Router for a Model."""

        if model is not None:
            self.model = model

        if registry is not None:
            self.registry = registry

        '''
        if fields is None:
            warnings.warn(
                '{} has no fields, defaulting to __all__ !'.format(self)
            )
            fields = '__all__'

        self.fields = fields
        '''

        for name, value in attributes.items():
            setattr(self, name, value)

        self.views = Views(self.generate_views(*(views or [])))

    def register(self):
        """
        Register to self.registry.

        Also, adds the get_absolute_url() method to the model class if it has
        None, to return the reversed url for this instance to the view of this
        Router with the ``detail`` slug.

        Set get_absolute_url in your model class to disable this feature. Until
        then, welcome in 2018.

        Also, register this router as default router for its model class in the
        RouterRegistry.
        """
        self.registry[self.model] = self

        for view in self.views:
            if view.urlname == 'detail':
                break
        if not self.views or view.urlname != 'detail':
            return

        if not hasattr(self.model, 'get_absolute_url'):
            def get_absolute_url(self):
                from crudlfap import crudlfap
                return crudlfap.site[type(self)]['detail'].clone(
                    object=self).url
            self.model.get_absolute_url = get_absolute_url

    def get_urlpatterns(self):
        """
        Generate URL patterns for this Router views.
        """
        return [view.urlpattern for view in self.views]

    def get_urlpattern(self):
        return path(self.urlpath, (
            [
                path('/', (
                    [v.urlpattern for v in self.views if v.urlpath],
                    None,
                    None
                ))
            ] + [v.urlpattern for v in self.views if not v.urlpath],
            self.app_name,
            self.namespace,
        ))

    def get_menu(self, name, request, **kwargs):
        """
        Return allowed view objects which have ``name`` in their ``menus``.

        For each view class in self.views which have ``name`` in their
        ``menus`` attribute, instanciate the view class with ``request`` and
        kwargs, call ``allowed()`` on it.

        Return the list of view instances for which ``allowed()`` has passed.
        """
        views = []

        for v in self.views:
            if name not in getattr(v, 'menus', []):
                continue

            view = v.clone(request=request, **kwargs)()

            if view.allowed:
                views.append(view)

        return views

    def get_model(self):
        return None

    def allowed(self, view):
        """
        Return True to allowed a access to a view.

        Called by the default view.allowed() implementation.

        If you override the view.allowed() method, then it's up to you
        to decide if you want to call this method or not.

        Returns True if user.is_staff by default.
        """
        if view.required_permissions:
            for permission in view.required_permissions:
                args = [view.object] if view.object_permission_check else []
                if not view.request.user.has_perm(permission, *args):
                    return False
        else:
            return view.request.user.is_staff
        return True

    def get_objects_for_user(self, user, perms):
        """Return the list of objects for a given set of perms."""
        return self.model.objects.all()

    def get_fields_for_user(self, user, perms, obj=None):
        """Return the list of fields for a user."""
        return [f.name for f in self.model._meta.fields]
