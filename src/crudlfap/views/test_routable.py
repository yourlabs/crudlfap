from crudlfap.test_routers import Artist
from crudlfap.utils import view_resolve
from crudlfap.views.generic import View

import pytest


class ExampleView(View):
    def allow(self, user):
        if not user.is_authenticated:
            return False

        if self.object.pk == 1:
            return True

        return user.is_staff


def test_example_view():
    assert ExampleView.get_slug() == 'example'
    assert ExampleView.get_url_pattern() == 'example/$'
    assert ExampleView.get_url_name() == 'example'


def test_derived_view():
    class DerivedView(ExampleView):
        pass
    assert DerivedView.get_slug() == 'derived'
    assert DerivedView.get_url_pattern() == 'derived/$'
    assert DerivedView.get_url_name() == 'derived'


def test_view_factory_with_slug():
    view = ExampleView.factory(slug='example3')
    assert view.get_slug() == 'example3'
    assert view.get_url_pattern() == 'example3/$'
    assert view.get_url_name() == 'example3'
    assert view.url().pattern._regex == 'example3/$'


def test_view_factory_with_model():
    view = ExampleView.factory(model=Artist)
    assert view.get_slug() == 'example'
    assert view.get_url_pattern() == 'example/$'
    assert view.get_url_name() == 'artist_example'
    assert view.url().pattern._regex == 'example/$'


def test_view_factory_with_and_slug():
    view = ExampleView.factory(model=Artist, slug='lol')
    assert view.get_slug() == 'lol'
    assert view.get_url_pattern() == 'lol/$'
    assert view.get_url_name() == 'artist_lol'
    assert view.url().pattern._regex == 'lol/$'


def test_view_factory_with_and_slug_and_prefix():
    view = ExampleView.factory(model=Artist, slug='lol', url_prefix='rofl/')
    assert view.get_slug() == 'lol'
    assert view.get_url_pattern() == 'lol/$'
    assert view.get_url_name() == 'artist_lol'
    assert view.url().pattern._regex == 'rofl/lol/$'


def test_view_factory_allow():
    from django.contrib.auth.models import AnonymousUser, User
    artist = Artist(pk=1)
    user = AnonymousUser()

    view = ExampleView.factory(object=artist)()
    assert not view.allow(user), 'forbid anonymous'

    user = User(is_staff=False)
    view = ExampleView.factory(object=artist)()
    assert view.allow(user), 'allow pk=1 for authed users'

    artist.pk = 12
    view = ExampleView.factory(object=artist)()
    assert not view.allow(user), 'forbid pk=12 for non staff'

    user = User(is_staff=True)
    view = ExampleView.factory(object=artist)()
    assert view.allow(user), 'allow any pk for staff'


urlpatterns = [
    ExampleView.url(),
    ExampleView.factory(slug='example2').url(),
    ExampleView.factory(slug='example3', url_name='example4').url(),
]


@pytest.mark.urls('crudlfap.views.test_routable')
def test_views_with_overrides():
    view = view_resolve('example')
    assert view.get_slug() == 'example'
    assert view.__name__ == ExampleView.__name__
    assert view.get_url_pattern() == 'example/$'

    view = view_resolve('example2')
    assert view.get_slug() == 'example2'
    assert view.get_url_pattern() == 'example2/$'

    view = view_resolve('example4')
    assert view.get_slug() == 'example3'
    assert view.get_url_pattern() == 'example3/$'
