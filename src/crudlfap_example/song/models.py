from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Song(models.Model):
    artist = models.ForeignKey('artist.artist', models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('title'))
    duration = models.IntegerField(default=320)
    owner = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
