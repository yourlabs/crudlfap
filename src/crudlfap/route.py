import inspect

from django import http
from django.urls import path, reverse, reverse_lazy
from django.utils.module_loading import import_string

from .factory import Factory
from .utils import guess_urlfield


class RouteMetaclass(type):
    router = None

    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}'.format(attr[4:], attr))

        getter = getattr(self, 'get_' + attr)

        if inspect.ismethod(getter):
            return getter()
        else:
            return getter(self)

    def get_app_name(self):
        return self.model._meta.app_label if self.model else None

    def get_model(self):
        return self.router.model if self.router else None

    def get_urlpath(self):
        return self.urlname

    def get_urlname(self):
        urlname = self.__name__.lower()
        if urlname.endswith('view'):
            urlname = urlname[:-4]
        elif urlname.endswith('route'):
            urlname = urlname[:-5]

        if self.model:
            model_name = self.model._meta.model_name.lower()
            if urlname.startswith(model_name):
                urlname = urlname[len(model_name):]

        if not urlname and self.model:
            urlname = self.model._meta.model_name

        return urlname or None

    def get_urlpattern(self):
        return path(self.urlpath, self.as_view(), name=self.urlname)

    def get_urlfullname(self):
        if self.router and self.registry:
            return '{}:{}:{}'.format(
                self.router.registry.app_name,
                self.router.namespace,
                self.urlname
            )
        elif self.registry:
            return '{}:{}'.format(
                self.registry.app_name,
                self.urlname
            )
        elif self.router:
            return '{}:{}'.format(
                self.router.namespace,
                self.urlname
            )
        else:
            return self.urlname

    def get_urlfield(self):
        if self.router and self.router.urlfield:
            return self.router.urlfield
        return guess_urlfield(self.model)


class Route(Factory, metaclass=RouteMetaclass):
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

    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}()'.format(attr[4:], attr))

        if hasattr(self, 'get_' + attr):
            return getattr(self, 'get_' + attr)()

        return getattr(type(self), attr)

    def get_required_permissions(self):
        return None

    def get_allowed(self):
        """
        Must return True if it dispatching this view is allowed.

        This means that the view should be instanciated with all the context it
        needs for this method to work.

        The best way for you to understand the pattern being this is this
        pseudo code::

            class SomeDetailView(DetailView):
                def get_context_data(self):
                    return dict(
                        # For the object used in this view instance, we would
                        # also have been allowed to execute the delete view
                        # with this request.
                        can_delete=SomeDeleteView(
                            object=self.object,
                            request=self.request,
                        ).allowed()
                    )

        This means that your view classes are ready for an allow() override
        which considers that the view object was instanciated with everything
        it would need to dispatch.

        By default, this proxies the router's allowed() method which
        returns True for staff users by default.  If the view has no router
        then it returns True if the request user is_staff.

        Override with a lambda in a factory if you want to open to all::

            YourView.factory(allowed=True)

        You can also set allow on the router if you want to allow a whole
        router::

            YourRouter(YourModel, allowed=True)
        """
        if not self.router:
            return self.request.user.is_staff

        if not self.router.allowed(self):
            return False

        return True

    def get_registry(self):
        if self.router:
            return self.router.registry
        from .site import site
        return site

    def get_login_url(self):
        if self.registry:
            return reverse('{}:login'.format(self.registry.app_name))
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Run allow() before dispatch(), because that's what its for."""
        if not self.allowed:
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
