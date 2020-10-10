from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import ugettext_lazy as _

from .registry import Registry
from .route import Route
from .views.generic import TemplateView


site = Registry(
    views=[
        Route.factory(
            LoginView,
            title_html=_('Login'),
            redirect_authenticated_user=True,
            authenticate=False,
        ),
        Route.factory(
            LogoutView,
            authenticate=False,
        ),
        TemplateView.clone(
            template_name='crudlfap/home.html',
            title=_('Home'),
            title_menu=_('Dashboard'),
            urlname='home',
            urlpath='',
            authenticate=False,
            material_icon='home',
        )
    ]
)
