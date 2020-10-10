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
            'class': 'ViewLink ' + 'active' if active else '',
            'tag': 'a',
        })

        for key, value in getattr(view, 'link_attributes', {}).items():
            attrs[key] = value.replace('"', '\\"')

        if not getattr(view, 'turbolinks', True):
            attrs['data-turbolinks'] = 'false'

        super().__init__(*content, **attrs)


class ListItem(Component):
    def __init__(self, *content, icon=None, meta=None, **attrs):
        attrs.setdefault('tag', 'mwc-list-item')
        attrs.setdefault('onclick', 'listSubmenuClick(this)')

        content = [
            Component(*content, tag='span'),
        ]

        if icon:
            content.append(
                Icon(icon, slot='graphic')
            )
            attrs.setdefault('graphic', 'icon')

        if meta:
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
            ListItem(
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
                ListItem(
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


class ViewListItem(ListItem):
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
                ViewListItem(crudlfap.site.views['home']),
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
                    ListItem(
                        _('Log in'),
                    ),
                    href=reverse('crudlfap:login')
                ),
            )
        else:
            content.append(
                A(
                    ListItem(
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
                        ListItem(
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
