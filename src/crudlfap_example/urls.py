from django.conf.urls import include, url
from django.views import generic
from django.contrib import admin

urlpatterns = [
    url(r'^basic/', include('crudlfap_example.basic.urls')),

    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^debug/', include('crudlfap.urls')),
    url(r'^$', generic.TemplateView.as_view(template_name='crudlfap/home.html')),
]
