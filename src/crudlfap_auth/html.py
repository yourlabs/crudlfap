from django.apps import apps
from django.urls import reverse
from django.contrib.sites.models import Site
from crudlfap.html import *  # noqa

User = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))


@template('registration/login.html', App)
class LoginFormViewComponent(FormContainer):
    demo = False

    def context(self, *content, **context):
        context['view'].title = 'Login'
        return super().context(*content, **context)

    def to_html(self, *content, view, form, **kwargs):
        site = Site.objects.get_current(view.request)
        content = content or [
            H2('Welcome to ' + site.name, style='text-align: center;'),
        ]
        return super().to_html(
            Form(
                *content,
                # OAuthConnect(),
                # Span('Or enter email and password:', cls='center-text'),
                CSRFInput(view.request),
                form,
                Div(
                    MDCButtonRaised('Continue'),
                    A(
                        MDCButtonOutlined('forgot password'),
                        href=reverse('password_reset')
                    ),
                    style='display: flex; justify-content: space-between',
                ),
                method='POST',
                action=view.request.path_info,
                cls='form card',
            ),
            cls='',
        )


@template('registration/logged_out.html', App)
class LogoutViewComponent(FormContainer):
    def context(self, *content, **context):
        context['view'].title = 'Logout'
        return super().context(*content, **context)

    def __init__(self, *content, **context):
        super().__init__(
            H4('You have been logged out'),
            Section(
                'Thank you for spending time on our site today.',
            ),
            Div(
                MDCButton('Login again', tag='a', href=reverse('login')),
                style='display:flex; justify-content: flex-end;',
            ),
            cls='card',
            style='text-align: center',
        )


@template('registration/password_reset_form.html', App)
class PasswordResetCard(FormContainer):
    def to_html(self, *content, view, form, **context):
        return super().to_html(
            H4('Reset your password', style='text-align: center;'),
            Form(
                CSRFInput(view.request),
                form,
                MDCButtonRaised('Reset password'),
                method='POST',
                cls='form',
            ),
            cls='card',
        )


@template('registration/password_reset_confirm.html', App)
class PasswordResetConfirm(FormContainer):
    def context(self, *content, **context):
        context['view'].title = 'Password reset confirm'
        return super().context(*content, **context)

    def to_html(self, *content, view, form, **context):
        return super().to_html(
            H4('Reset your password', style='text-align: center;'),
            Form(
                CSRFInput(view.request),
                form,
                MDCButtonRaised('confirm'),
                method='POST',
                cls='form',
            ),
            cls='card',
        )


@template('registration/password_reset_complete.html', App)
class PasswordResetComplete(FormContainer):
    def __init__(self, **context):
        super().__init__(
            H4('Your password have been reset', cls='center-text'),
            Div(
                'You may go ahead and ',
                A('log in', href=reverse('login')),
                ' now',
            ),
        )


@template('registration/password_reset_done.html', App)
class PasswordResetDone(FormContainer):
    def __init__(self, **context):
        super().__init__(
            H4('A link has been sent to your email address'),
            A('Go to login page', href=reverse('login')),
            cls='card',
            style='text-align: center;',
        )
