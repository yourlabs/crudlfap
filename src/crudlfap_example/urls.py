from django.conf.urls import include, url
from django.views import generic

urlpatterns = [
    url(r'^artist/', include('crudlfap_example.artist.urls')),

    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^debug/', include('crudlfap.urls')),
    url(r'^$', generic.TemplateView.as_view(
        template_name='crudlfap/home.html')),
]
