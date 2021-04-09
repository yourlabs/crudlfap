from django.utils.translation import ugettext_lazy as _

from .registry import Registry
from .views.generic import TemplateView
from .views.api import SchemaView

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
        ),
        SchemaView,
        TemplateView.clone(
            icon='api',
            template_name='crudlfap/api.html',
            menus=['main'],
            title=_('API'),
            title_menu=_('Api'),
            title_heading='',
            urlname='api',
            urlpath='api',
            authenticate=False,
        ),
    ]
)
