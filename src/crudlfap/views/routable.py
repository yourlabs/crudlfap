"""
Routable Views are fun.

A view can reverse and generate its own URL::

    urlpatterns = [ExampleView.url()]

This means it must know its url pattern and name or how to generate them, but
that doesn't mean you can't override them::

    urlpatterns = [
        ExampleView.factory(
            url_pattern='yoururlpattern/$',
            url_name='yoururlname',
        ).url()
    ]

The problem with all this magic is that then you loose the ability to read the
truck load of urls.py that you have written manually to find your view or debug
things. To compensate for this, consider using : we offer lovely debug views in
crudflap.views.debug.
"""


import re

from django import http
from django.conf.urls import url
from django.urls import reverse_lazy


class RoutableViewMixin(object):
    """
    Let your view route itself.

    RoutableView differ from Django Views because they have a slug class
    attribute. This slug may be defined in the view class or is autocalculated
    based on the view class name. The slug is then used to generate the default
    url name and patterns, which you might has well want to override.

    The view may have a model, in which case it will prefix the url name with
    it.

    All the following attributes are optionnal, but if you want to override
    some of them you don't have to create a subclass: just use
    RoutableView.factory(), it will dynamically create the subclass for you.

    .. py:attribute:: slug

        Slug name of this view, often properly automatically generated
        from view class name uppon registration.

    .. py:attribute:: url_pattern

        URL pattern to use for this view.

    .. py:attribute:: url_prefix

        Prefix for the URL pattern of this view.

    .. py:attribute:: url_name

        Name for the URL this view should return in url().

    .. py:attribute:: model

        Optionnal model class, used to prefix url_name if set.

    .. py:attribute:: router

        If you're using the CRUDLFA+ Router to register a View, then this will
        be automatically populated when the Router instanciates. So far, it's
        only used in get_url_prefx() to get the url_prefix that the router for
        this view might have. But you should probably use it to also return the
        default form_class, fields, and so on, which is what CRUDLFA+ generic
        views do.
    """
    url_pattern = None
    url_prefix = None
    url_name = None
    model = None
    router = None

    @classmethod
    def factory(cls, **attributes):
        """
        Return a subclass with the given attributes.

        Ie.::

            class YourModelListView(ListView):
                model = Foo
            urlpatterns = [YourModelListView.url()]

        Becomes as easy as::

            urlpatterns = [ListView.factory(model=YourModel).url()]
        """
        name = cls.__name__
        model = attributes.get('model', None)
        if model is None:
            model = getattr(cls, 'model', None)
        if model and model.__name__ not in cls.__name__:
            name = '{}{}'.format(model.__name__, cls.__name__)
        return type(name, (cls,), attributes)

    @classmethod
    def url(cls):
        """
        Return the Django url object.

        This class method does not take any argument, and won't pass any when
        calling as_view(). Instead, you can use factory() as such::

            urlpatterns = [ListView.factory(model=Lul, paginate_by=10).url()]
        """
        return url(
            '{}{}'.format(
                cls.get_url_prefix(),
                cls.get_url_pattern(),
            ),
            cls.as_view(),
            name=cls.get_url_name(),
        )

    @classmethod
    def get_url_prefix(cls):
        """
        Return the router prefix or the view's url_prefix.

        Prepended to get_url_pattern() by url().
        """
        url_prefix = getattr(cls, 'url_prefix', '')
        if not url_prefix and getattr(cls, 'router', None):
            url_prefix = cls.router.url_prefix
        return url_prefix or ''

    @classmethod
    def get_url_pattern(cls):
        """Return the url pattern for this view."""
        if cls.url_pattern:
            return cls.url_pattern.format(cls.get_slug())
        return '{}/$'.format(cls.get_slug())

    @classmethod
    def get_slug(cls):
        """
        Return the view class slug.

        Strip model (if any) class name and 'View' suffix from view class name.
        Ie. YourModelCreateView gets the 'create' slug.
        """
        slug = getattr(cls, 'slug', None)
        if slug:
            return slug

        name = cls.__name__
        model = getattr(cls, 'model', None)
        if model:
            name = name.replace(model.__name__, '')

        name = name.replace('View', '')
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @classmethod
    def get_url_name(cls):
        """Return the url name for this view."""
        url_name = getattr(cls, 'url_name', None)
        if url_name:
            return url_name

        parts = []
        model = getattr(cls, 'model', None)
        if model:
            parts.append(model._meta.model_name)
        parts.append(cls.get_slug())
        return '_'.join(parts)

    @classmethod
    def to_url_args(cls, *args):  # pylint: disable=unused-argument
        """
        Return url reverse args given these args.

        This method makes it possible to transform or add args passed to
        reverse() before they are used.
        """
        return args

    @classmethod
    def reverse(cls, *args):
        """Reverse a url to this view with the given args."""
        return reverse_lazy(cls.get_url_name(), args=cls.to_url_args(*args))

    def get_url_args(self):
        """
        Return args for reversing this view url from self.

        See ``self_reverse()`` for detail.
        """
        return []

    @property
    def href(self):
        """
        Return the URL for this view given its current state.

        Given that the ``reverse()`` method is a class method, this should
        allow things like::

            url = YourView(object=your_object).url
        """
        return self.reverse(*self.get_url_args())

    def allow(self):
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
                        ).allow()
                    )

        This means that your view classes are ready for an allow() override
        which considers that the view object was instanciated with everything
        it would need to dispatch.

        By default, this proxies the router's allow() method which returns True
        for staff users by default.  If the view has no router then it returns
        True if the request user is_staff.

        Override with a lambda in a factory if you want to open to all::

            YourView.factory(allow=lambda v: True)

        You can also set allow on the router if you want to allow a whole
        router::

            YourRouter(YourModel, allow=lambda r, v: True)
        """
        if not self.router:
            return self.request.user.is_staff
        return self.router.allow(self)

    def dispatch(self, request, *args, **kwargs):
        """Run allow() before dispatch(), because that's what its for."""
        if not self.allow():
            return http.HttpResponseNotFound()
        return super().dispatch(request, *args, **kwargs)
