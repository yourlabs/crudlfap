import logging

from crudlfap import crudlfap

from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django import http


logger = logging.getLogger()


class PasswordView(crudlfap.UpdateView):
    slug = 'password'
    material_icon = 'vpn_key'
    color = 'purple darken-4'
    controller = 'modal'
    action = 'click->modal#open'

    def get_form_class(self):
        if self.object == self.request.user:
            cls = PasswordChangeForm
        else:
            cls = SetPasswordForm
        # This fixes the form messages feature from UpdateView
        return type(cls.__name__, (cls,), dict(instance=self.object))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs


class BecomeUser(crudlfap.ObjectView):
    urlname = 'su'
    menus = ['object']
    material_icon = 'attach_money'
    color = 'pink darken-4'

    def get_object(self, queryset=None):
        user = super().get_object()

        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
        else:
            messages.error(
                self.request,
                'Could not find user {}'.format(self.kwargs['username'])
            )

        return user

    def get(self, request, *a, **k):
        logger.info('BecomeUser by {}'.format(self.request.user))
        become_user = request.session.get('become_user', request.user.pk)
        new_user = self.get_object()
        if new_user:
            auth.login(request, new_user)
            request.session['become_user'] = become_user
            messages.info(
                request,
                'Switched to user {}'.format(new_user)
            )

        # FUTURE: #23 redirect to / when request.path permissions are not ok for new_user
        # return http.HttpResponse('<script type="text/javascript">history.back()</script>')
        return http.HttpResponseRedirect('/' + self.router.registry.urlpath)


class Become(crudlfap.View):
    urlname = 'su'

    def allow(self):
        return 'become_user' in self.request.session

    def get_object(self):
        user = self.model.objects.get(pk=self.request.session['become_user'])
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        return user

    def get(self, request, *a, **k):
        logger.info('Become by {}'.format(self.request.user))
        if 'become_user' not in request.session:
            logger.debug('No become_user in session {}'.format(self.request.user))
            return http.HttpResponseNotFound()

        if 'become_user' in request.session:
            user = self.get_object()
            auth.login(request, user)
            messages.info(
                request,
                'Switched back to your user {}'.format(
                    user
                )
            )
            if 'become_user' in request.session.keys():
                del request.session['become_user']
        else:
            messages.warning(
                request,
                'Your are still superuser {}'.format(self.request.user)
            )

        return http.HttpResponseRedirect('/' + self.registry.urlpath)
