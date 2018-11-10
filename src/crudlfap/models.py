from crudlfap.site import site as default_site

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from lookupy import Collection


class ControllerManager(models.Manager):
    def __init__(self, site=None):
        super().__init__()
        self.site = site or default_site

    def get_queryset(self):
        items = [
            Controller.factory(i) for i in self.site.values()
        ]
        return Collection(items)


class Controller(models.Model):
    router = models.Field()
    model = models.Field()
    app = models.Field()

    objects = ControllerManager()

    class Meta:
        managed = False

    def __str__(self):
        return self.pk

    @classmethod
    def factory(cls, router):
        return cls(
            pk=f'{router.model._meta.app_label}.{router.model.__name__}',
            router=router,
            app=str(router.model._meta.app_config.verbose_name),
            model=str(router.model._meta.verbose_name).capitalize(),
        )


class URLManager(models.Manager):
    def __init__(self, site=None):
        super().__init__()
        self.site = site or default_site

    def get_queryset(self):
        views = [
            URL.factory(i) for i in self.site.views
        ]

        for router in self.site.values():
            views += [
                URL.factory(i) for i in router.views
            ]

        return Collection(views)


class URL(models.Model):
    controller = models.ForeignKey(
        Controller,
        on_delete=models.SET_NULL,
        null=True,
    )
    urlpath = models.Field()
    fullurlpath = models.Field()
    urlname = models.Field()
    urlfullname = models.Field()
    view = models.Field()
    model = models.Field()

    objects = URLManager()

    class Meta:
        managed = False

    def __str__(self):
        return self.view.label

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.view.model)

    @property
    def codename(self):
        if not self.view.model:
            return self.view.permission_shortcode
        return '_'.join((
            self.view.permission_shortcode,
            self.view.model.__name__.lower(),
        ))

    def get_or_create_permission(self):
        return Permission.objects.update_or_create(
            content_type=self.content_type,
            codename=self.codename,
            defaults=dict(
                name=getattr(
                    self.view,
                    'title_menu',
                    self.view.permission_shortcode
                ),
            )
        )[0]

    @classmethod
    def factory(cls, view):
        kwargs = dict(
            pk=f'{view.__name__}',
            view=view,
            urlpath=view.urlpath,
            urlname=view.urlname,
            urlfullname=view.urlfullname,
        )

        if view.model:
            kwargs['model'] = view.model

        if view.router:
            kwargs['controller'] = Controller.factory(view.router)
            kwargs['fullurlpath'] = '/'.join((
                view.router.registry.urlpath,
                view.router.urlpath,
                view.urlpath,
            ))

        url = cls(**kwargs)
        return url
