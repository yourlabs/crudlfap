from django.urls import reverse

from crudlfap import html


def registration(request, menu):
    if not request.user.is_authenticated:
        menu.insert(1, html.A(
            html.MDCListItem('Signup', icon='badge'),
            href=reverse('django_registration_register'),
            style='text-decoration: none',
        ))
    return menu


html.mdcDrawer.menu_hooks.append(registration)
