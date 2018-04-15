from django.conf import settings
from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def readable(self, user):
        if user.is_staff or user.is_superuser:
            return self

        published = models.Q(publish__lte=timezone.now())

        if not user.is_authenticated:
            return self.filter(published)

        return self.filter(models.Q(owner=user) | published)

    def editable(self, user):
        if not user.is_authenticated:
            return self.none()

        if user.is_staff or user.is_superuser:
            return self

        return self.filter(owner=user)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)


class Post(models.Model):
    name = models.CharField(max_length=100, verbose_name='title')
    publish = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        on_delete=models.CASCADE,
    )

    objects = PostManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def editable(self, user):
        return user.is_staff or user.is_superuser or user == self.owner
