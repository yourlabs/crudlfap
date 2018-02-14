"""
CRUDLFA+ router for Django 2.0.

Note that you can also use non-database backed models, by inheriting from
models.Model and setting their Meta.managed attribute to False. Then, you can
use CRUDLFA+ views and routers.
"""
import collections
import warnings

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.utils.module_loading import import_string

from .views.routable import RoutableViewMixin

crudlfap = apps.get_app_config('crudlfap')  # pylint: disable=invalid-name


class RouterRegistry(collections.OrderedDict):
    """Registers Routers which have generated urlpatterns in this thread."""

    def get_app_menus(self, name, request, **kwargs):
        """Sort Router instances by app name."""
        result = collections.OrderedDict()
        for model, router in self.items():
            menu = router.get_menu(name, request, **kwargs)

            if not menu:
                continue

            app = apps.get_app_config(model._meta.app_label)
            result.setdefault(app, [])
            result[app].append(router)
        return result

    def __getitem__(self, arg):
        """Return a router instance by model class, instance or dotted name."""
        from django.db import models
        if isinstance(arg, models.Model):
            arg = type(arg)
        if isinstance(arg, str):
            arg = apps.get_model(*arg.split('.'))
        return super().__getitem__(arg)


class Router(object):
    """
    Base router for CRUDLFA+ RoutableView.

    .. py:attribute:: model

        Optional model class for this Router and all its views.

    .. py:attribute:: url_prefix

        Optional url prefix for all of this Router's views.
    """

    registry = RouterRegistry()

    views = crudlfap.get_default_views()

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

            Router(Artist).generate_views(
                [CreateView, dict(_cls=DetailView, extra_stuff='bar')]
            )
        """
        result = []
        for arg in views or self.views:
            view = arg

            if isinstance(view, str):
                view = import_string(view)

            try:
                if not issubclass(view, RoutableViewMixin):
                    view = type(view.__name__, (view, RoutableViewMixin), {})
            except Exception as e:
                print('Got an error with view:', view)
                raise e

            view = view.factory(
                model=self.model,
                router=self,
            )

            # Set this after setting the model in the factory() call above
            view.slug = view.get_slug()
            if view.slug in self.menu_map:
                view.menus.extend(self.menu_map[view.slug])

            result.append(view)
        return result

    def __init__(self, model=None, url_prefix=None, fields=None,
                 url_field=None, views=None, menu_map=None, **attributes):

        """Create a Router for a Model."""
        self.model = model
        self.url_prefix = url_prefix or ''
        self.menu_map = menu_map or {}

        if self.model and not url_field:
            try:
                self.model._meta.get_field('slug')
            except FieldDoesNotExist:
                url_field = 'pk'
            else:
                url_field = 'slug'
        self.url_field = url_field

        if fields is None:
            warnings.warn(
                '{} has no fields, defaulting to __all__ to get out of your'
                ' way, but this is not secure because it means users can see'
                ' and edit any field, which is not necessarily secure,'
                ' depending on your model.'
                ' If this is really what you want, please set fields="__all__"'
                ' at the router level'.format(self)
            )
            fields = '__all__'
        self.fields = fields

        # Save the user a type() call, really ? mehh
        for name, value in attributes.items():
            setattr(self, name, value)

        self.views = self.generate_views(*(views or []))

    def __getitem__(self, slug):
        """Get a view by slug."""
        for view in self.views:
            if view.get_slug() == slug:
                return view

        raise KeyError(
            'View with slug {} not in router {}'.format(
                slug,
                type(self).__name__,
            )
        )

    def urlpatterns(self):
        """
        Generate URL patterns for this Router views.

        Also, adds the get_absolute_url() method to the model class if it has
        None, to return the reversed url for this instance to the view of this
        Router with the ``detail`` slug.

        Set get_absolute_url in your model class to disable this feature. Until
        then, welcome in 2017.

        Also, register this router as default router for its model class in the
        RouterRegistry.
        """
        self.registry[self.model] = self

        if not hasattr(self.model, 'get_absolute_url'):
            def get_absolute_url(self):
                return Router.registry[type(self)]['detail'].reverse(self)

            self.model.get_absolute_url = get_absolute_url

        return [view.url() for view in self.views]

    def get_menu(self, name, request, **kwargs):
        """
        Return allowed view objects which have ``name`` in their ``menus``.

        For each view class in self.views which have ``name`` in their
        ``menus`` attribute, instanciate the view class with ``request`` and
        kwargs, call ``allow()`` on it.

        Return the list of view instances for which ``allow()`` has passed.
        """
        views = []

        for v in self.views:
            if name not in getattr(v, 'menus', []):
                continue

            view = v.factory(request=request, **kwargs)()

            if view.allow():
                views.append(view)

        return views

    def allow(self, view):
        """
        Return True to allow a access to a view.

        Called by the default view.allow() implementation.

        If you override the view.allow() method, then it's up to you
        to decide if you want to call this method or not.

        Returns True if user.is_staff by default.
        """
        return view.request.user.is_staff


class RouterList(collections.MutableSequence):
    def __init__(self, *routers, **index_opts):
        self._routers = list(routers)
        self._urlpatterns = None
        self.add_index_url = index_opts.get('add_index_url', False)
        self.index_name = index_opts.get('index_name', '')
        self.index_menu = index_opts.get('index_menu', 'index')
        self.index_template = index_opts.get(
            'index_template', 'crudlfap/app_index.html'
        )
        self.index_view = index_opts.get(
            'index_view', 'crudlfap.views.generic.AppIndexView'
        )
        super().__init__()

    def __setitem__(self, index, value):
        self._routers[index] = value
        self.reset_urlpatterns()

    def __delitem__(self, index):
        del self._routers[index]
        self.reset_urlpatterns()

    def insert(self, index, value):
        self._routers.insert(index, value)
        self.reset_urlpatterns()

    def __getitem__(self, index):
        return self._routers[index]

    def __len__(self):
        return len(self._routers)

    def get_index_view(self):
        return import_string(self.index_view)

    def get_index_as_view(self):
        vc = self.get_index_view()
        return vc.as_view(routers=self._routers, index_name=self.index_name,
                          template_name=self.index_template)

    def get_index_urlpattern(self):
        from django.conf.urls import url

        pattern = url(r'^$', self.get_index_as_view(),
                      name=self.index_name.lower() + '_index')
        return pattern

    def urlpatterns(self):
        if self._urlpatterns is None:
            self._urlpatterns = []
            if self.add_index_url:
                self._urlpatterns.append(self.get_index_urlpattern())
            for router in self._routers:
                self._urlpatterns.extend(router.urlpatterns())
        return self._urlpatterns

    def reset_urlpatterns(self):
        if self._urlpatterns is not None:
            self._urlpatterns = None
