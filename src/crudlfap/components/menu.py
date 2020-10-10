from crudlfap import shortcuts as crudlfap
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ryzom.components import (
    A, Div, Icon, Li, Text, Ul
)

from ryzom.components import Component


class Icon(Component):
    def __init__(self, name, **attrs):
        super().__init__(name, tag='mwc-icon', **attrs)


class NavMenu(Component):
    def __init__(self, request):
        active = request.path_info == crudlfap.site.views['home'].url
        content = [MenuItem(crudlfap.site.views['home'], request)]

        content = []
        for app, routers in crudlfap.site.get_app_menus(
                'main', request).items():
            for router in routers:
                views = router.get_menu('model', request)
                if len(views) == 1:
                    view = views[0]

                    content.append(
                        MenuItem(view, request, single_item=True)
                    )
                else:
                    content.append(MenuRouter(router, request))
                    for view in router.get_menu('model', request):
                        content.append(MenuItem(view, request, submenu=1))

        if not request.user.is_authenticated:
            content.append(
                Component(
                    A(_('Log in'), href=reverse('crudlfap:login')),
                    **{'tag': 'mwc-list-item', 'class': ''},
                )
            )
        else:
            content.append(Component(
                A(
                    _('Log out'),
                    **{
                        'data-noprefetch': 'true',
                        'href': reverse('crudlfap:logout'),
                    }
                ),
                **{'tag': 'mwc-list-item', 'class': ''}
            ))

            if request.session.get('become_user', None):
                content.append(Li(
                    A(
                        ' '.join([
                            str(_('Back to your account')),
                            request.session['become_user_realname'],
                        ]),
                        **{
                            'data-noprefetch': 'true',
                            'href': reverse('crudlfap:su'),
                        }
                    ),
                    **{'class': ''}
                ))

        super().__init__(
            *content,
            **{
                'tag': 'mwc-list',
                'class': 'crudlfap.components.menu.NavMenu',
            }
        )


class ListItem(Component):
    def __init__(self, view, request, single_item=False, graphic=None):
        if single_item:
            span = (Text(
                str(view.router.model._meta.verbose_name_plural.capitalize()))
            )
        elif getattr(view, 'router', None) is None:
            span = (Text(str(getattr(view, 'title', str(view)))))
        elif getattr(view.router, 'model', None) is None:
            span = (Text(str(getattr(view, 'title', str(view)))))
        else:
            span = (
                Text(str(view.title_menu.capitalize()))
            )

        content = [Component(span, tag='span')]
        attrs = dict(tag='mwc-list-item')

        show_icon = view if not single_item else view.router
        if getattr(show_icon, 'material_icon', ''):
            content.append(
                Icon(show_icon.material_icon, slot='graphic'),
            )
            attrs['graphic'] = graphic or 'icon'

        super().__init__(*content, **attrs)


class MenuItem(Component):
    def __init__(self, view, request, single_item=False, submenu=None):
        attrs = {
            'href': view.url,
            'title': str(view.title_link),
            'class': 'MenuItem active' if request.path_info == view.url else '',
            'tag': 'a',
        }

        if submenu:
            attrs['hidden'] = 'true'
            attrs['submenu'] = 'true'

        for key, value in getattr(view, 'link_attributes', {}).items():
            attrs[key] = value.replace('"', '\\"')

        if not getattr(view, 'turbolinks', True):
            attrs['data-turbolinks'] = 'false'

        return super().__init__(
            ListItem(view, request, single_item=single_item, graphic='medium' if submenu else 'icon'),
            **attrs
        )


class MenuRouter(Component):
    def __init__(self, router, request):
        self.active = ''
        for view in router.get_menu('model', request):
            if view.url == request.path_info:
                self.active = 'active'

        content = []
        content.append(
            Component(str(router.model._meta.verbose_name_plural.capitalize()), tag='span'),
        )
        if getattr(router, 'material_icon', ''):
            content.append(Icon(router.material_icon, slot='graphic'))

        super().__init__(
            *content,
            **{
                'onclick': 'toggleSubmenu(this)',
                'class': '',
                'tag': 'mwc-list-item',
                'graphic': 'icon',
            }
        )
