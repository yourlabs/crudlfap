from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import ugettext_lazy as _

from .registry import Registry
from .route import Route
from .views.debug import UrlsView
from .views.generic import TemplateView


site = Registry(
    views=[
        Route.factory(
            LoginView,
            title_html=_('Login'),
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
            allowed=True,
        )
    ]
)
