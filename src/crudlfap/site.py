from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .registry import Registry
from .views.debug import UrlsView
from .views.generic import TemplateView


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
        TemplateView.as_view(
            template_name='crudlfap/home.html'
        )
    ),
]

site.views.append(UrlsView)
