from django.contrib.auth.views import LoginView, LogoutView

from .registry import Registry
from .route import Route
from .views.debug import UrlsView
from .views.generic import TemplateView


site = Registry(
    views=[
        Route.factory(
            LoginView,
            redirect_authenticated_user=True,
            allowed=True,
        ),
        Route.factory(LogoutView),
        UrlsView,
        TemplateView.clone(
            template_name='crudlfap/home.html',
            title_heading='',
            urlname='home',
            urlpath='',
        )
    ]
)
