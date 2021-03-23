from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import ugettext_lazy as _

from .registry import Registry
from .route import Route
from .views.generic import TemplateView


site = Registry(
    views=[
        Route.factory(
            LoginView,
            title=_('Login'),
            title_submit=_('Login'),
            title_menu=_('Login'),
            menus=['main'],
            redirect_authenticated_user=True,
            authenticate=False,
            icon='login',
            has_perm=lambda self: not self.request.user.is_authenticated,
        ),
        Route.factory(
            LogoutView,
            menus=['main'],
            title=_('Logout'),
            title_submit=_('Logout'),
            title_menu=_('Logout'),
            icon='logout',
            authenticate=False,
            has_perm=lambda self: self.request.user.is_authenticated,
        ),
        TemplateView.clone(
            icon='home',
            template_name='crudlfap/home.html',
            menus=['main'],
            title=_('Home'),
            title_menu=_('Home'),
            title_heading='',
            urlname='home',
            urlpath='',
            authenticate=False,
        )
    ]
)
