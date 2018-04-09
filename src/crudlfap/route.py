from django import http
from django.urls import re_path, reverse_lazy

from .factory import Factory
from .utils import guess_urlfield


class RouteMetaclass(type):
    router = None

    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}'.format(attr[4:], attr))

        return getattr(self, 'get_' + attr)()

    def get_app_name(self):
        return self.model._meta.app_label if self.model else None

    def get_model(self):
        return self.router.model if self.router else None

    def get_urlregex(self):
        return self.urlname + '$'

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
        u = self.urlregex
        regex = u if u.endswith('$') else u + '$'
        return re_path(regex, self.as_view(), name=self.urlname)

    def get_urlfullname(self):
        return '{}:{}'.format(self.router.namespace, self.urlname)

    def get_urlfield(self):
        if self.router and self.router.urlfield:
            return self.router.urlfield
        return guess_urlfield(self.model)


class Bridge(object):
    def __init__(self, name, getter=None):
        self.name = name
        self.getter = getter or 'get_' + name

    def __get__(self, ins, typ):
        if ins:
            return getattr(ins, self.getter)()
        else:
            return getattr(typ, self.getter)(typ())


class Route(Factory, metaclass=RouteMetaclass):
    url = Bridge('url')
    urlargs = Bridge('urlargs')
    allowed = Bridge('allowed')
    required_permissions = Bridge('required_permissions')

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

    def dispatch(self, request, *args, **kwargs):
        """Run allow() before dispatch(), because that's what its for."""
        if not self.allowed:
            return http.HttpResponseNotFound()
        return super().dispatch(request, *args, **kwargs)
