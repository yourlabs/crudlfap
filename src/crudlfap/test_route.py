import re

from crudlfap_example.artist.models import Artist

from django.views import generic

from .route import Route
from .router import Router


def test_model():
    route = Route.clone(model=Artist)
    assert route.model == Artist


def test_model_router_fallback():
    route = Router(Artist, fields='__all__', views=[Route]).views[0]
    assert route.model == Artist


def test_urlname():
    route = Route.clone(urlname='foo')
    assert route.urlname == 'foo'


def test_urlname_from_name():
    class FooRoute(Route):
        pass
    assert FooRoute.urlname == 'foo'


def test_urlpath():
    route = Route.clone(urlpath='foo')
    assert route.urlpath == 'foo'


def test_urlpath_from_urlname():
    class FooRoute(Route):
        pass
    assert FooRoute.urlpath == 'foo'


def test_urlpattern():
    class DetailView(generic.DetailView, Route):
        model = Artist
    p = DetailView.urlpattern
    assert p.name == 'detail'
    assert p.pattern.regex == re.compile('^detail$')
    assert p.callback.view_class == DetailView
