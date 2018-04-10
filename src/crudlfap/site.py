from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.urls import include, path

from .registry import Registry
from .views.generic import TemplateView
from .views.debug import UrlsView


site = Registry()

site.extra_urls = [
    path(
        'login',
        LoginView.as_view(redirect_authenticated_user=True),
        name='login',
    ),
    path(
        'logout',
        LogoutView.as_view(),
        name='logout',
    ),
    path(
        'urls',
        UrlsView.as_view(),
        name='crudlfap_urls',
    ),
    path(
        '',
        generic.TemplateView.as_view(
            template_name='crudlfap/home.html'
        )
    ),
]

site.views.append(UrlsView)
