# flake8: noqa: N805
"""
CRUDLFA+ introduces an MVC-ish pattern, as the Router class is meant to sit
between a Model class and its set of View. Your views will have to inherit from
Route to work in Router.views. This structural decision made for you by
CRUDLFA+ was not exactly designed: it's an open source rewrite of a module that
was ordered in a proprietary project.
"""
import re

from django import http
from django.urls import path, reverse, reverse_lazy
from django.utils.module_loading import import_string

from .factory import Factory, FactoryMetaclass
from .utils import guess_urlfield


class RouteMetaclass(FactoryMetaclass):
    """Base autocalculations for views.

    .. py:data:: app_name

        The view's app name.

    .. py:data:: model

        The view's model if any.

    .. py:data:: urlpath

        The path for the url path definition.

    .. py:data:: label

        The view label, serves as key in a Router.views.

    .. py:data:: urlpattern

        The Django URL path() instance, for inclusion in url lists.

    .. py:data:: urlfullname

        The full name to reverse the URL, with namespaces if any.

    .. py:data:: urlfield

        The default model field that will be use to match in the URL. It can be
        pk, or name, slug ...
    """
    router = None

    def get_app_name(cls):
        """Return the model's app_name or None."""
        return cls.model._meta.app_label if cls.model else None

    def get_model(cls):
        """Return the router's model or None."""
        return cls.router.model if cls.router else None

    def get_urlpath(cls):
        """Return the urlname."""
        return cls.urlname

    def get_urlname(cls):
        """Return a string that can be used as url name."""
        urlname = cls.__name__.lower()
        if urlname.endswith('view'):
            urlname = urlname[:-4]
        elif urlname.endswith('route'):
            urlname = urlname[:-5]

        if cls.model:
            model_name = cls.model._meta.model_name.lower()
            if urlname.startswith(model_name):
                urlname = urlname[len(model_name):]

        if not urlname and cls.model:
            urlname = cls.model._meta.model_name

        return urlname or None

    def get_label(cls):
        """Return a readable label for this view.

        Strips View and Route from class name, also removes the model class
        name if it finds it: for YourModelUpdateView this returns `update`.
        """
        name = re.sub('(View|Route)$', '', cls.__name__)
        if cls.model:
            name = re.sub('^' + cls.model.__name__, '', name)
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>", name)

    def get_urlpattern(cls):
        """Return the Django URL object to include in a urlpatterns."""
        return path(cls.urlpath, cls.as_view(), name=cls.urlname)

    def get_urlfullname(cls):
        """Return the url name eventually with router and site namespaces."""
        if cls.router and cls.registry:
            return '{}:{}:{}'.format(
                cls.router.registry.app_name,
                cls.router.namespace,
                cls.urlname
            )
        elif cls.registry:
            return '{}:{}'.format(
                cls.registry.app_name,
                cls.urlname
            )
        elif cls.router:
            return '{}:{}'.format(
                cls.router.namespace,
                cls.urlname
            )
        else:
            return cls.urlname

    def get_urlfield(cls):
        """Return the router urlfield if any, else guess_urlfield()"""
        if cls.router and cls.router.urlfield:
            return cls.router.urlfield
        return guess_urlfield(cls.model)


class Route(Factory, metaclass=RouteMetaclass):
    """The mixin for Views that will make it compatible with Router.

    .. py:data:: authenticate

        False by default, it makes the default has_perm() implementation
        require Django permission.

    .. py:data:: urlargs

        Args that should be passed to reverse() along with Route.urlfullname.

    .. py:data:: url

        Absolute url to the view, relying on Route.urlfullname and
        Route.urlargs.

    You will be able to check if a user has access to a view with a given
    object for example as such::

        crudlfap.site[YourModel]['detail'].clone(
            request=request,
            object=obj,
        ).has_perm()

    If you want to open a View to all, set authenticate=False, examples::

        class YourDetailView(DetailView):
            authenticate = False

        class YourRouter(Router):
            views = [
                YourDetailView,
                ListView.clone(authenticate=False),  # example with clone
            ]

    Without authenticate=False, the default has_perm() implementation requires the
    request user to have the permission corresponding to the
    permission_fullcode attribute.

    To create the permission with permission_fullcode, you can browse in your
    CRUDLFA+ site and navigate to URL list view, for each URL you have link in
    the menu called "authorized" that lets you select which groups have this
    permission: it will auto-create the permission in the database if
    necessary.
    """

    @classmethod
    def reverse(cls, *args, **kwargs):
        """Reverse a url to this view with the given args."""
        return reverse_lazy(cls.urlfullname, args=args, kwargs=kwargs)

    def get_urlargs(self):
        """
        Return args for reversing this view url from self.
        See ``self.reverse()`` for detail.
        """
        return []

    def get_url(self):
        """
        Return the URL for this view given its current state.
        Given that the ``reverse()`` method is a class method, this should
        allow things like::
            url = YourView(object=your_object).url
        """
        return self.reverse(*self.urlargs)

    def get_permission_shortcode(self):
        """Return the middle part for the view permission.

        Returns the urlname by default.
        """
        return self.urlname

    def get_permission_codename(self):
        """Return the codename attribute for the view Permission."""
        if not self.model:
            return self.permission_shortcode
        return f'{self.permission_shortcode}_{self.model._meta.model_name}'

    def get_permission_fullcode(self):
        """
        Return a string with the app name, permission_shortcode and model name.
        """
        return f'{self.app_name}.{self.permission_codename}'

    def get_authenticate(self):
        return True

    def has_perm(self):
        """Checks for user permission."""
        if not self.authenticate:
            return True

        return self.request.user.has_perm(self.permission_fullcode, self)

    def get_registry(self):
        if self.router:
            return self.router.registry
        from .site import site
        return site

    def get_login_url(self):
        if self.registry:
            return reverse('{}:login'.format(self.registry.app_name))
        return reverse('login')

    def get_allowed_groups(self):
        if not self.router:
            return []
        return getattr(self.router, 'allowed_groups', [])

    def dispatch(self, request, *args, **kwargs):
        """This will run has_perm prior to super().dispatch()."""
        if not self.has_perm():
            if not request.user.is_authenticated:
                return http.HttpResponseRedirect(
                    self.login_url + '?next=' + request.path_info
                )
            else:
                return http.HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    @classmethod
    def factory(cls, view, **attributes):
        if isinstance(view, str):
            view = import_string(view)
        return type(view.__name__, (view, cls), attributes)
