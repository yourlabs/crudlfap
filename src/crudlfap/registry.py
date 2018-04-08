import collections

from django.apps import apps
from django.urls import re_path


class Registry(collections.OrderedDict):
    lazy_properties = [
        'app_name',
        'namespace',
        'regex',
        'urlpattern',
        'urlpatterns',
    ]

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

    def __getattr__(self, attr):
        if attr in self.lazy_properties:
            return getattr(self, 'get_' + attr)()
        raise AttributeError(attr)

    def __init__(self, *a):
        self.views = []
        super().__init__(*a)

    def get_urlpatterns(self):
        return [
            router.urlpattern for router in self.values()
        ] + [view.urlpattern for view in self.views]

    def get_urlpattern(self):
        return re_path(self.regex + '/', (
            self.urlpatterns,
            self.app_name,
            self.namespace,
        ))

    def get_app_name(self):
        return None

    def get_namespace(self):
        return None

    def get_regex(self):
        return ''
