from crudlfap import shortcuts as crudlfap

from django.conf import settings
from django.urls import include, path, re_path

urlpatterns = [
    crudlfap.site.urlpattern,
    path('bundles/', include('ryzom_django.bundle')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
