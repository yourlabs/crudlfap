# flake8: noqa: N805
"""
Most black magic for views are defined in the crudlfap.route module.

CRUDLFA+ introduces a new design pattern for views that came out during
refactoring sessions from a corporate project, and re-written for Django 2.0
from scratch. L
"""
import re

from django import http
from django.urls import path, reverse, reverse_lazy
from django.utils.module_loading import import_string

from .factory import Factory, FactoryMetaclass
from .utils import guess_urlfield


class RouteMetaclass(FactoryMetaclass):
    router = None

    def get_app_name(cls):
        return cls.model._meta.app_label if cls.model else None

    def get_model(cls):
        return cls.router.model if cls.router else None

    def get_urlpath(cls):
        return cls.urlname

    def get_urlname(cls):
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
        name = re.sub('(View|Route)$', '', cls.__name__)
        if cls.model:
            name = re.sub('^' + cls.model.__name__, '', name)
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>", name)

    def get_urlpattern(cls):
        return path(cls.urlpath, cls.as_view(), name=cls.urlname)

    def get_urlfullname(cls):
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
        if cls.router and cls.router.urlfield:
            return cls.router.urlfield
        return guess_urlfield(cls.model)


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

    def get_required_permissions(self):
        return [self.full_permission_code]

    def get_short_permission_code(self):
        return self.urlname

    def get_full_permission_code(self):
        return '{}.{}_{}'.format(
            self.app_name,
            self.short_permission_code,
            self.model._meta.model_name
        )

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

        Override allowed if you want to open to all::

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
