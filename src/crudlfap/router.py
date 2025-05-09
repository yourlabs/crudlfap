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
from django.db import models
from django.urls import path
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from crudlfap import html

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
        if len(self):
            first = self[0]
            kwargs = dict()
            if model := getattr(first, 'model', None):
                kwargs['model'] = model
            if router := getattr(first, 'router', None):
                kwargs['router'] = router
            value = value.clone(**kwargs)

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

    .. py:attribute:: views

        :py:class:`ViewsDescriptor` using
        :py:data:`~crudlfap.settings.CRUDLFAP_VIEWS` by default,
        otherwise your list of views.

        .. note:: The final views list is generated by the
                  :py:meth:`generate_views` method.

    .. py:attribute:: fields

        Fields that views should use by default.

    .. py:attribute:: json_fields

        Fields that the Router serializer should use by default.
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
        from crudlfap.site import site
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

    def get(self, urlname, *args):
        try:
            return self[urlname]
        except KeyError:
            if args:
                return args[0]
            raise

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
        then, you got it for free.

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
                from crudlfap import shortcuts as crudlfap
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
        kwargs, call ``has_perm()`` on it.

        Return the list of view instances for which ``has_perm()`` has passed.
        """
        views = []

        for v in self.views:
            if name not in getattr(v, 'menus', []):
                continue

            view = v.clone(request=request, **kwargs)()

            if view.has_perm():
                views.append(view)

        return views

    def get_menu_component(self, name, request, **kwargs):
        views = self.get_menu(name, request, **kwargs)
        buttons = []
        for view in views:
            button = html.Component(
                mark_safe(f'<button class="material-icons mdc-icon-button" ryzom-id="308bade28a8c11ebad3800e18cb957e9" style="color: {getattr(view, "color", "")}; --mdc-ripple-fg-size:28px; --mdc-ripple-fg-scale:1.7142857142857142; --mdc-ripple-left:10px; --mdc-ripple-top:10px;">{getattr(view, "icon", "")}</button>'),  # noqa
                title=view.title.capitalize(),
                href=view.url + '?_next=' + request.path_info,
                style='text-decoration: none',
                tag='a',
            )
            if getattr(view, 'controller', None) == 'modal':
                button.attrs.up_layer = 'new'
                button.attrs.up_accept_location = view.router['list'].url
            else:
                button.attrs['up-target'] = html.A.attrs['up-target']
            button.attrs.update(getattr(view, 'link_attributes', {}))
            buttons.append(button)
        return html.Div(*buttons)

    def get_model(self):
        return None

    def has_perm(self, view):
        """
        Override this method if you don't use a Django permission backend.

        This method is called by the default has_perm implementation of the
        Route.
        This method returns the result of view.has_perm_backend() by default.

        As such, if you use a Django permission backend such as
        crudlfap_auth.backends.ViewBackend then might not need to override this
        method.
        """
        return view.has_perm_backend()

    def get_queryset(self, view):
        """Return the queryset for a view, returns all by default."""
        return self.model.objects.all()

    def get_fields(self, view):
        """Return the list of fields for a user."""
        fields = list(self.model._meta.fields)
        fields += list(self.model._meta.local_many_to_many)
        return [f.name for f in fields]

    def get_allowed_groups(self):
        return []

    def get_swagger_model_name(self, request):
        return self.model.__name__

    def get_swagger_model_definition(self, request):
        result = dict(
            properties={},
            type='object',
            # TODO:
            # 'required': ['name', 'photoUrls'],
        )
        for field in self.model._meta.fields:
            res = getattr(self, 'swagger_field_{field.name}_definition', None)
            if res:
                result['properties'][field.name] = res
                continue

            field_def = dict()
            # relate to one model
            # field_def = {'$ref': '#/definitions/' + field.model.__name__}

            int_fields = (
                models.IntegerField,
                models.PositiveIntegerField,
            )
            if isinstance(field, int_fields):
                field_def['type'] = 'integer'
            elif isinstance(field, models.BooleanField):
                field_def['type'] = 'boolean'
            elif isinstance(field, models.JSONField):
                field_def['type'] = 'object'
            else:
                field_def['type'] = 'string'

            result['properties'][field.name] = field_def
        return result

    def get_json_fields(self):
        return [
            f.name for f in self.model._meta.fields
        ]

    def get_FIELD_json(self, obj, field):
        value = getattr(obj, field)
        if callable(value):
            value = value()
        if type(value) in self.registry:
            value = self.registry[type(value)].serialize(value)
        elif value and not isinstance(value, (str, int, float, bool)):
            value = str(value)
        return value

    def serialize(self, obj, fields=None):
        fields = fields or self.json_fields
        return {
            field: getattr(
                self,
                f'get_{field}_json',
                self.get_FIELD_json,
            )(obj, field)
            for field in self.json_fields
        }
