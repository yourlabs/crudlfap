from crudlfap import shortcuts as crudlfap
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ryzom.components import (
    A, Div, Icon, Li, Text, Ul
)


class NavMenu(Ul):
    def __init__(self, request):
        content = [
            MenuHome(request),
        ]

        if not request.user.is_authenticated:
            content.append(
                Li(
                    A(_('Log in'), href=reverse('crudlfap:login')),
                    **{'class': 'no-padding'},
                )
            )
        else:
            content.append(Li(
                A(
                    _('Log out'),
                    **{
                        'class': 'waves-effect',
                        'data-noprefetch': 'true',
                        'href': reverse('crudlfap:logout'),
                    }
                ),
                **{'class': 'no-padding'}
            ))

            if request.session.get('become_user', None):
                content.append(Li(
                    A(
                        ' '.join([
                            str(_('Back to your account')),
                            request.session['become_user_realname'],
                        ]),
                        **{
                            'class': 'waves-effect',
                            'data-noprefetch': 'true',
                            'href': reverse('crudlfap:su'),
                        }
                    ),
                    **{'class': 'no-padding'}
                ))

        super().__init__(
            *content,
            **{
                'class': 'sidenav sidenav-fixed',
                'id': 'slide-out',
            }
        )


class MenuItem(Li):
    def __init__(self, view, request, single_item=False):
        attrs = {
            'class': 'waves-effect',
            'href': view.url,
            'title': str(view.title_link),
        }
        for key, value in getattr(view, 'link_attributes', {}).items():
            attrs[key] = value.replace('"', '\\"')

        if not getattr(view, 'turbolinks', True):
            attrs['data-turbolinks'] = 'false'

        content = []

        show_icon = view if not single_item else view.router

        if getattr(show_icon, 'material_icon', ''):
            content.append(
                Icon(show_icon.material_icon),
            )

        if single_item:
            content.append(Text(
                str(view.router.model._meta.verbose_name_plural.capitalize()))
            )
        elif getattr(view, 'router', None) is None:
            content.append(Text(str(getattr(view, 'title', str(view)))))
        elif getattr(view.router, 'model', None) is None:
            content.append(Text(str(getattr(view, 'title', str(view)))))
        else:
            content.append(
                Text(str(view.title_menu.capitalize()))
            )

        super().__init__(
            A(*content, **attrs),
            **{'class': 'active' if request.path_info == view.url else ''}
        )


class MenuRouter(Li):
    def __init__(self, router, request):
        self.active = ''
        for view in router.get_menu('model', request):
            if view.url == request.path_info:
                self.active = 'active'

        sublinks = [Ul(
            *[MenuItem(view, request) for view in router.get_menu(
                'model', request)
              ]
        )]
        router_link_content = []
        if getattr(router, 'material_icon', ''):
            router_link_content.append(Icon(router.material_icon))
        router_link_content.append(
            Text(str(router.model._meta.verbose_name_plural.capitalize())),
        )

        content = [Ul(
            Li(
                A(
                    *router_link_content,
                    **{'class': 'collapsible-header waves-effect waves-teal'},
                ),
                Div(
                    *sublinks,
                    **{'class': 'collapsible-body'}
                ),
                **{'class': self.active}
                ),
            **{'class': 'collapsible collapsible-accordion'}
        )]

        super().__init__(
            *content,
            **{'class': 'no-padding'}
        )


class MenuHome(Li):
    def __init__(self, request):
        active = request.path_info == crudlfap.site.views['home'].url
        content = [MenuItem(crudlfap.site.views['home'], request)]

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

        super().__init__(
            *content,
            **{'class': 'no-padding' + ' active' if active else '', }
        )
