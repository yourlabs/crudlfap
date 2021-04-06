from django.conf import settings
from django.urls import include, path, re_path

from crudlfap import shortcuts as crudlfap

urlpatterns = [
    crudlfap.site.urlpattern,
    path('auth/', include('django.contrib.auth.urls')),
    path('bundles/', include('ryzom_django.bundle')),
]

# CRUDLFA+ extras
if 'crudlfap_registration' in settings.INSTALLED_APPS:
    urlpatterns.append(
        path(
            'registration/',
            include('django_registration.backends.activation.urls')
        ),
    )

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# PUBLIC DEMO mode
from django.contrib.auth.views import LoginView  # noqa
from django.contrib.auth.models import User  # noqa


def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        for name in ('admin', 'staff', 'user'):
            user = User.objects.filter(username=name).first()
            if not user:
                user = User(username=name, email='user@example.com')
            if name == 'staff':
                user.is_staff = True
            if name == 'admin':
                user.is_superuser = True
            user.set_password(name)
            user.save()
    return LoginView.as_view()(request, *args, **kwargs)
urlpatterns.insert(0, path('auth/login/', login_view, name='login'))  # noqa


from crudlfap_auth.html import *  # noqa
@template('registration/login.html', App)  # noqa
class DemoLogin(LoginFormViewComponent):
    def to_html(self, *content, **context):
        return super().to_html(
            H3('Demo mode enabled'),
            P('Login with either username/password of:'),
            Ul(
                Li('user/user: for user'),
                Li('staff/staff: for staff'),
                Li('admin/admin: for superuser (technical stuff should appear)'),  # noqa
            ),
            *content,
            **context,
        )
