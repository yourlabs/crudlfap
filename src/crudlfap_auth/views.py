"""
Crudlfa+ PasswordView, Become and BecomeUser views.

Crudlfa+ takes views further than Django and are expected to:

- generate their URL definitions and reversions,
- check if a user has permission for an object,
- declare the names of the navigation menus they belong to.
"""

import logging

from crudlfap import shortcuts as crudlfap

from django import http
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger()


class PasswordView(crudlfap.UpdateView):
    slug = 'password'
    material_icon = 'vpn_key'
    color = 'purple darken-4'
    controller = 'modal'
    action = 'click->modal#open'

    def get_title_submit(self):
        return _('update').capitalize()

    def get_form_class(self):
        if self.object == self.request.user:
            cls = PasswordChangeForm
        else:
            cls = SetPasswordForm
        # This fixes the form messages feature from UpdateView
        return type(cls.__name__, (cls,), dict(instance=self.object))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object
        return kwargs


class BecomeUser(crudlfap.ObjectView):
    urlname = 'su'
    menus = ['object']
    material_icon = 'attach_money'
    color = 'pink darken-4'
    link_attributes = {'data-noprefetch': 'true'}

    def become(self):
        """
        Implement this method to override the default become logic.
        """
        auth.login(self.request, self.object, backend=self.backend)

    def get_title_menu(self):
        return _('become').capitalize()

    def get_object(self, queryset=None):
        user = super().get_object()

        if user:
            user.backend = self.backend
        else:
            messages.error(
                self.request,
                'Could not find user {}'.format(self.kwargs['username'])
            )

        return user

    def get(self, request, *a, **k):
        logger.info('BecomeUser by {}'.format(self.request.user))
        request_user = request.user
        self.request = request
        result = self.become()
        if 'become_user' not in request.session:
            request.session['become_user_realname'] = str(request_user)
            request.session['become_user'] = str(request_user.pk)
        messages.info(
            request,
            _('Switched to user %s') % request.user
        )
        return result if result else http.HttpResponseRedirect(
            '/' + self.router.registry.urlpath)

    def get_backend(self):
        return 'django.contrib.auth.backends.ModelBackend'


class Become(crudlfap.View):
    urlname = 'su'

    def has_perm(self):
        return 'become_user' in self.request.session

    def get_backend(self):
        return 'django.contrib.auth.backends.ModelBackend'

    def get_object(self):
        user = self.model.objects.get(pk=self.request.session['become_user'])
        user.backend = self.backend
        return user

    def get(self, request, *a, **k):
        logger.info('Become by {}'.format(self.request.user))
        if 'become_user' not in request.session:
            logger.debug(
                'No become_user in session {}'.format(self.request.user))
            return http.HttpResponseNotFound()

        user = self.get_object()
        auth.login(request, user)
        messages.info(
            request,
            _('Switched back to your user %s') % user
        )
        return http.HttpResponseRedirect('/' + self.registry.urlpath)
