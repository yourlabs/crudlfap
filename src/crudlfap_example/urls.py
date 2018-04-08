from crudlfap import crudlfap

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.views import LoginView
from django.views import generic

urlpatterns = crudlfap.site.urlpatterns + [
    # CRUDLFA+ examples, we favor new include with registry
    # url(r'^artist/', include('crudlfap_example.artist.urls')),
    # url(r'^song/', include('crudlfap_example.song.urls')),
    # url(r'^nondb/', include('crudlfap_example.nondb.urls')),

    # url(r'^auth/', include('crudlfap_user.urls')),

    url(r'^auth/login/', LoginView.as_view(redirect_authenticated_user=True)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^debug/', include('crudlfap.urls')),
    url(r'^$', generic.TemplateView.as_view(
        template_name='crudlfap/home.html')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
