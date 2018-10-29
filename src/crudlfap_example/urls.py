from crudlfap import crudlfap

from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [crudlfap.site.urlpattern]

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
