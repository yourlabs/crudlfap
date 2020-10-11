from crudlfap import shortcuts as crudlfap
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ryzom.components import (
    A, Div, Icon, Li, Text, Ul
)

from ryzom.components import Component


class ViewLink(Component):
    def __init__(self, view, *content, active=False, **attrs):
        attrs.update({
            'href': view.url,
            'title': str(view.title_link),
            'data-controller': getattr(view, 'controller', ''),
            'data-action': getattr(view, 'action', ''),
            'class': 'ViewLink ' + 'active' if active else '',
            'tag': 'a',
        })

        for key, value in getattr(view, 'link_attributes', {}).items():
            attrs[key] = value.replace('"', '\\"')

        if not getattr(view, 'turbolinks', True):
            attrs['data-turbolinks'] = 'false'

        super().__init__(*content, **attrs)


class MenuItem(Component):
    def __init__(self, *content, icon=None, meta=None, **attrs):
        attrs.setdefault('tag', 'mwc-list-item')

        content = [
            Component(*content, tag='span'),
        ]

        if icon:
            content.append(
                Icon(icon, slot='graphic')
            )
            attrs.setdefault('graphic', 'icon')

        if meta:
            attrs.setdefault('onclick', 'listSubmenuClick(this)')
            content.append(
                Icon(
                    meta,
                    slot='meta',
                    onclick='metaSubmenuClick(this)',
                )
            )
            attrs.setdefault('hasMeta', 'true')

        super().__init__(*content, **attrs)


class RouterMenu(ViewLink):
    def __init__(self, request, router):
        self.request = request
        self.router = router
        self.menu = router.get_menu('model', request)

        self.index = getattr(router, 'index', self.menu[-1])

        active = ''
        for view in self.menu:
            if view.url == request.path_info:
                active = 'active'

        attrs = {
            'active': 'active',
        }
        super().__init__(
            self.index,
            MenuItem(
                Text(router.model._meta.verbose_name_plural.capitalize()),
                icon=getattr(router, 'material_icon', None),
                meta='keyboard_arrow_down' if len(self.menu) > 1 else None,
            ),
            **attrs,
        )

    def submenus(self):
        return [
            ViewLink(
                view,
                MenuItem(
                    Text(view.title_menu.capitalize()),
                    icon=getattr(view, 'material_icon', None),
                    graphic='medium',
                ),
                hidden='true',
                visible='false',
                #active=request.path_info == view.url,
            )
            for view in self.menu
            if view is not self.index
        ]


class ViewMenuItem(MenuItem):
    def __init__(self, view, graphic=None):
        #if getattr(view, 'router', None) is None:
        #    span = (Text(str(getattr(view, 'title', str(view)))))
        #elif getattr(view.router, 'model', None) is None:
        #    span = (Text(str(getattr(view, 'title', str(view)))))
        #else:

        content = [Text(view.title_menu.capitalize())]
        attrs = dict(
            tag='mwc-list-item',
            icon=getattr(view, 'material_icon', None)
        )

        super().__init__(*content, **attrs)


class Icon(Component):
    def __init__(self, name, **attrs):
        attrs['class'] = 'material-icons'
        super().__init__(name, tag='span', **attrs)


class NavMenu(Component):
    def __init__(self, request):
        content = [
            ViewLink(
                crudlfap.site.views['home'],
                ViewMenuItem(crudlfap.site.views['home']),
                active=request.path_info == crudlfap.site.views['home'].url,
            )
        ]

        menu = crudlfap.site.get_app_menus('main', request)
        for app, routers in menu.items():
            for router in routers:
                content.append(RouterMenu(request, router))
                content += content[-1].submenus()

        if not request.user.is_authenticated:
            content.append(
                A(
                    MenuItem(
                        _('Log in'),
                    ),
                    href=reverse('crudlfap:login')
                ),
            )
        else:
            content.append(
                A(
                    MenuItem(
                        _('Log out'),
                    ),
                    **{
                        'data-noprefetch': 'true',
                        'href': reverse('crudlfap:logout'),
                    }
                ),
            )

            if request.session.get('become_user', None):
                content.append(
                    A(
                        MenuItem(
                            ' '.join([
                                str(_('Back to your account')),
                                request.session['become_user_realname'],
                            ]),
                        ),
                        **{
                            'data-noprefetch': 'true',
                            'href': reverse('crudlfap:su'),
                        }
                    ),
                )

        super().__init__(
            *content,
            **{
                'tag': 'mwc-list',
                'class': 'crudlfap.components.menu.NavMenu',
            }
        )


class TopMenu(Component):
    def __init__(self, request, views):
        content = [
            ViewLink(
                view,
                Component(
                    icon=view.material_icon,
                    tag='mwc-icon-button',
                    outlined='true',
                    style='color: ' + getattr(view, 'color', 'white'),
                )
            )
            for view in views
        ]

        super().__init__(
            *content,
            **{
                'tag': 'div',
                'class': 'crudlfap.components.menu.TopMenu',
                'slot': 'actionItems',
                'style': 'display: flex; align-items: center',
            }
        )
