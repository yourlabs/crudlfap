from django.db import models


class SongRatingManager(models.Manager):
    object_list = []


class SongRating(models.Model):
    song = models.ForeignKey('song.Song', on_delete=models.DO_NOTHING)
    rating = models.IntegerField()

    objects = SongRatingManager()

    class Meta:
        managed = False

    def __str__(self):
        return '{}: {}'.format(self.song, self.rating)

    def save(self):
        if self.pk:
            return  # already in memory

        object_list = type(self).objects.object_list
        self.pk = len(object_list) + 1
        object_list.append(self)

    def delete(self):
        type(self).objects.object_list = [
            o for o in type(self).objects.object_list
            if o.pk != self.pk
        ]
