import collections

from django.apps import apps
from django.urls import path

from .router import ViewsDescriptor


crudlfap = apps.get_app_config('crudlfap')  # pylint: disable=invalid-name


class Registry(collections.OrderedDict):
    views = ViewsDescriptor()

    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}()'.format(attr[4:], attr))

        if hasattr(self, 'get_' + attr):
            return getattr(self, 'get_' + attr)()

        raise AttributeError('{} or get_{}()'.format(attr, attr))

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
        elif isinstance(arg, str) and '.' in arg:
            arg = apps.get_model(*arg.split('.'))
        return super().__getitem__(arg)

    def __init__(self, views=None, *a, **attrs):
        self.views = views or []
        super().__init__(*a)
        for k, v in attrs.items():
            setattr(self, k, v)

    def get_urlpatterns(self):
        for view in self.views:
            view.registry = self

        return [
            router.urlpattern for router in self.values()
        ] + [view.urlpattern for view in self.views]

    def get_urlpattern(self):
        urlpath = self.urlpath
        if urlpath and not urlpath.endswith('/'):
            urlpath += '/'

        return path(urlpath, (
            self.urlpatterns,
            self.app_name,
            self.namespace,
        ))

    def get_app_name(self):
        return 'crudlfap'

    def get_namespace(self):
        return None

    def get_urlpath(self):
        return ''

    def get_title(self):
        return 'CRUDLFA+'

    def get_navbar_color(self):
        return 'teal darken-3'
