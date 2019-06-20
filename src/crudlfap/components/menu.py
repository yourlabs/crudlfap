from crudlfap import shortcuts as crudlfap
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from ryzom.components import Component, A, Div, Ul, Li, Span, Input, Button, Text


class Icon(Component):
    def __init__(self, icon):
        return super().__init__('i', [Text(icon)], {'class': 'material-icons'})


class FutureMixin:
    def __init__(self, *content, **attrs):
        if 'cls' in attrs:
            attrs['class'] = attrs.pop('cls')  # support HTML class attr

        content = [
            c if hasattr(c, 'to_html') else Text(str(c))
            for c in content
        ]

        return super().__init__(
            list(content),
            attrs,
            attrs.pop('events', None),
            attrs.pop('parent', None),
            attrs.pop('_id', None),
        )


class A2(FutureMixin, A):
    pass
A2 = type('A2', (FutureMixin, A), {})  # for reference


class Li2(FutureMixin, Li):
    pass


class Menu(Ul):
    def __init__(self, request):
        content = [
            MenuHome(request),
        ]

        if not request.user.is_authenticated:
            content.append(
                Li2(
                    A2(_('Log in'), href=reverse('crudlfap:login')),
                    cls='no-padding',
                )
            )
        else:
            content.append(Li2(A2(
                _('Log out'),
                **{
                    'class': 'waves-effect',
                    'data-noprefetch': 'true',
                    'href': reverse('crudlfap:logout'),
                }
            ), cls='no-padding'))

            if request.session.get('become_user', None):
                content.append(Li2(A2(
                    ' '.join([
                        str(_('Back to your account')),
                        request.session['become_user_realname'],
                    ]),
                    **{
                        'class': 'waves-effect',
                        'data-noprefetch': 'true',
                        'href': reverse('crudlfap:su'),
                    }
                ), cls='no-padding'))

        return super().__init__(
            content,
            {
                'class': 'sidenav sidenav-fixed',
                'id': 'slide-out',
            }
        )


class MenuItem(Li):
    def __init__(self, view, request):
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
        if getattr(view, 'material_icon', ''):
            content.append(
                Icon(view.material_icon),
            )

        if getattr(view, 'router', None) is None:
            content.append(Text(str(getattr(view, 'title', str(view)))))
        elif getattr(view.router, 'model', None) is None:
            content.append(Text(str(getattr(view, 'title', str(view)))))
        else:
            content.append(
                Text(
                    str(view.title_menu.capitalize())
                )
            )

        super().__init__(
            [
                A(
                    content,
                    attrs,
                )
            ],
            {
                'class': 'active' if request.path_info == view.url else ''
            }
        )


class MenuRouter(Li2):
    def __init__(self, router, request):
        self.active = ''
        for view in router.get_menu('model', request):
            if view.url == request.path_info:
                self.active = 'active'

        sublinks = [
            Ul(
                [MenuItem(view, request) for view in router.get_menu('model', request)]
            )
        ]
        router_link_content = []
        if getattr(router, 'material_icon', ''):
            router_link_content.append(Icon(router.material_icon))
        router_link_content.append(
            Text(
                str(router.model._meta.verbose_name_plural.capitalize())
            ),
        )

        content = [Ul([
            Li([
                A(
                    router_link_content,
                    {'class': 'collapsible-header waves-effect waves-teal'},
                ),
                Div(
                    sublinks,
                    {'class': 'collapsible-body'}
                )
            ], {
            'class': self.active
            })
        ], {
            'class': 'collapsible collapsible-accordion'
        })]

        return super().__init__(*content, cls='no-padding')



class MenuHome(Li):
    def __init__(self, request):
        active = request.path_info == crudlfap.site.views['home'].url
        content = [MenuItem(crudlfap.site.views['home'], request)]

        for app, routers in crudlfap.site.get_app_menus('main', request).items():
            for router in routers:
                views = router.get_menu('model', request)
                if len(views) == 1:
                    view = views[0]

                    content.append(
                        MenuItem(view, request)
                    )
                else:
                    content.append(MenuRouter(router, request))

        return super().__init__(
            content,
            {
                'class': 'no-padding' + ' active' if active else '',
            }
        )
