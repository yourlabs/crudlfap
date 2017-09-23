from django.db import models
from django.utils.translation import ugettext_lazy as _


class Song(models.Model):
    artist = models.ForeignKey('artist.artist', models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('title'))
    duration = models.IntegerField(default=320)
    upload = models.FileField(upload_to='songs')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
