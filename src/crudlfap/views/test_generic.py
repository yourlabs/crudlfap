import re

from crudlfap.test_routers import Artist
from crudlfap.utils import view_reverse
from crudlfap.views.generic import View

import pytest


class ExampleView(View):
    pass


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
    assert view.url().regex == re.compile('example3/$')


def test_view_factory_with_model():
    view = ExampleView.factory(model=Artist)
    assert view.get_slug() == 'example'
    assert view.get_url_pattern() == 'example/$'
    assert view.get_url_name() == 'artist_example'
    assert view.url().regex == re.compile('example/$')


def test_view_factory_with_and_slug():
    view = ExampleView.factory(model=Artist, slug='lol')
    assert view.get_slug() == 'lol'
    assert view.get_url_pattern() == 'lol/$'
    assert view.get_url_name() == 'artist_lol'
    assert view.url().regex == re.compile('lol/$')


def test_view_factory_with_and_slug_and_prefix():
    view = ExampleView.factory(model=Artist, slug='lol', url_prefix='rofl/')
    assert view.get_slug() == 'lol'
    assert view.get_url_pattern() == 'lol/$'
    assert view.get_url_name() == 'artist_lol'
    assert view.url().regex == re.compile('rofl/lol/$')


urlpatterns = [
    ExampleView.url(),
    ExampleView.factory(slug='example2').url(),
    ExampleView.factory(slug='example3', url_name='example4').url(),
]


@pytest.mark.urls('crudlfap.views.test_generic')
def test_view_with_slug():
    view = view_reverse('example')
    assert view.get_slug() == 'example'
    assert view.__name__ == ExampleView.__name__
    assert view.get_url_pattern() == 'example/$'

'''
@pytest.mark.urls('crudlfap.views.test_generic')
def test_view_with_slug():
    view = view_reverse('example2')
    assert view == ExampleView
'''
