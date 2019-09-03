from crudlfap import shortcuts as crudlfap

from django.conf import settings
from django.urls import include, re_path
from django.views.static import serve

urlpatterns = [
    crudlfap.site.urlpattern,
    re_path(
        r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'),
        serve,
        kwargs=dict(document_root=settings.STATIC_ROOT)
    ),
]
if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
