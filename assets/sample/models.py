from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """A Post model with name, description, publish and owner fields."""
    name = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(verbose_name='Description')
    publish = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return string name."""
        return self.name
