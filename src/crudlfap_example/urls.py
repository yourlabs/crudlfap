from django.conf import settings
from django.urls import include, path, re_path

from crudlfap import shortcuts as crudlfap

urlpatterns = [
    crudlfap.site.urlpattern,
    path('auth/', include('django.contrib.auth.urls')),
    path('bundles/', include('ryzom_django.bundle')),
]

# CRUDLFA+ extras
if 'crudlfap_registration' in settings.INSTALLED_APPS:
    urlpatterns.append(
        path(
            'registration/',
            include('django_registration.backends.activation.urls')
        ),
    )

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
