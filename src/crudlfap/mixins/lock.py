import datetime

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import timeago


class LockMixin(object):
    """Currently implements soft lock."""
    locks = False

    def get_deadlock_delta(self):
        return datetime.timedelta(**self.deadlock_delta_kwargs)

    def get_deadlock_delta_kwargs(self):
        return dict(seconds=30)

    def get_lock_key(self):
        return 'lock-{}'.format(self.url)

    def get_lock_value(self):
        return cache.get(self.lock_key)

    def get_locked(self):
        if not self.locks:
            return False
        value = self.lock_value
        if not value:
            return False
        if value['datetime'] + self.deadlock_delta < timezone.now():
            # expired lock
            cache.delete(self.lock_key)
            return False
        return True

    def get_locked_message(self):
        return _('Page was open by {} {}').format(
            self.lock_value.get('username', _('unknown user')),
            timeago.format(
                timezone.now() - self.lock_value['datetime'],
                getattr(self.request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
            )
        )

    def get(self, request, *args, **kwargs):
        if self.locked:
            messages.warning(request, self.locked_message)
        if self.locks:
            self.lock()
        return super().get(request, *args, **kwargs)

    def lock(self):
        value = dict(datetime=timezone.now())
        if self.request.user.is_authenticated:
            value['username'] = self.request.user.username
        cache.set(self.lock_key, value)
