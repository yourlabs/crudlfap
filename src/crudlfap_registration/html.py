from django.apps import apps
from django.urls import reverse
from crudlfap.html import *  # noqa

User = apps.get_model(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))


@template('django_registration/registration_form.html', App)
class RegistrationFormViewComponent(FormContainer):
    def to_html(self, *content, view, form, **context):
        return super().to_html(
            *content,
            H1('Looks like you need to register', cls='center-text'),
            Form(
                CSRFInput(view.request),
                form,
                MDCButtonRaised('Register'),
                method='POST',
                cls='form card',
            ),
        )


@template('django_registration/registration_complete.html', App)
class RegistrationCompleteNarrowCard(FormContainer):
    def __init__(self, **context):
        super().__init__(
            H4('Check your emails to finish !'),
            Div(
                'An activation link has been sent to your email address, '
                + 'please open it to finish the signup process.',
                style='margin-bottom: 24px',
            ),
            Div(
                'Then, come back and login to participate to your election.',
                style='margin-bottom: 24px;',
            ),
            cls='card',
            style='text-align: center',
        )


@template('django_registration/activation_complete.html', App)
class ActivationCompleteNarrowCard(FormContainer):
    def __init__(self, **context):
        super().__init__(
            H4('Your account has been activated !'),
            Div(
                'You may now ',
                A('login', href=reverse('login')),
                style='margin-bottom: 24px',
            ),
            cls='card',
            style='text-align: center',
        )


@template('django_registration/activation_failed.html', App)
class ActivationFailureNarrowCard(FormContainer):
    def __init__(self, **context):
        super().__init__(
            H4('Account activation failure'),
            Div(
                'Most likely your account has already been activated.',
                style='margin-bottom: 24px',
            ),
            cls='card',
            style='text-align: center',
        )
