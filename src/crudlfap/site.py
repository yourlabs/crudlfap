from django.utils.translation import ugettext_lazy as _

from .registry import Registry
from .views.generic import TemplateView

site = Registry(
    views=[
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
