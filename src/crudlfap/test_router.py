from crudlfap import crudlfap
from crudlfap.crudlfap import site

from crudlfap_example.artist.models import Artist

from django.db import models
from django.urls import resolve, reverse
from django.views import generic

import pytest

from .route import Route
from .router import Router


class TestRouter(Router):
    fields = '__all__'


def test_views():
    router = TestRouter()
    view = crudlfap.TemplateView.clone(urlname='home')
    router.views = [view]
    assert router.views['home'] == view
    assert router.views[0].urlname == 'home'

    router.views['home'] = router.views['home'].clone(template_name='lol')
    assert router.views['home'].template_name == 'lol'

    del router.views['home']
    assert len(router.views) == 0


def test_urlfield():
    assert Router().urlfield is None


def test_urlfield_with_model():
    class TestModel(models.Model):
        pass
    assert Router(model=TestModel).urlfield == 'pk'


def test_urlfield_with_slug():
    class TestModel(models.Model):
        slug = models.CharField(max_length=100)
    assert Router(model=TestModel).urlfield == 'slug'


def test_namespace_none():
    assert Router().namespace is None


def test_namespace():
    assert Router(namespace='lol').namespace == 'lol'


def test_namespace_with_model():
    assert Router(model=Artist).namespace == 'artist'


def test_path():
    assert Router(urlpath='foo').urlpath == 'foo'


def test_path_with_model():
    assert Router(model=Artist).urlpath == 'artist'


def test_app_name():
    assert Router(app_name='lol').app_name == 'lol'


def test_app_name_with_model():
    assert Router(model=Artist).app_name == 'artist'


def test_registry_default():
    assert Router().registry == site


def test_registry():
    site = dict()
    assert Router(registry=site).registry == site


class DetailView(Route, generic.DetailView):
    menus = ['object']

    # Not setting this would require
    # request.user.has_perm('artist.detail_artist', obj) to pass
    allowed = True

    # This is done by crudlfap generic ObjectView, but here tests django
    # generic views
    def get_urlargs(self):
        # This may be executed with just the class context (self.object
        # resolving to type(self).object, as from
        # Route.clone(object=something).url
        return [self.object.name]


@pytest.fixture
def router():
    return Router(model=Artist, views=[DetailView])


def test_getitem(router):
    assert issubclass(router['detail'], DetailView)


def test_urlpatterns(router):
    assert len(router.urlpatterns) == 1
    assert router.urlpatterns[0].name == 'detail'


def test_urlpattern(router):
    assert reverse('detail', router) == '/detail'
    assert resolve('/detail', router).func.view_class == router.views[0]


@pytest.mark.django_db
def test_get_menu(router, srf):
    a = Artist(name='a')
    from crudlfap_auth.crudlfap import User
    srf.user = User.objects.create(is_staff=True)
    req = srf.get('/')
    result = router.get_menu('object', req, object=a)
    assert len(result) == 1
    assert isinstance(result[0], DetailView)
    assert result[0].urlargs == ['a']
    assert type(result[0]).urlargs == ['a']
    assert str(result[0].url) == '/artist/a'

    b = type(result[0]).clone(object=a)
    assert str(b.url) == '/artist/a'
