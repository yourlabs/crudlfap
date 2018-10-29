from crudlfap_example.artist.models import Artist

from .factory import Factory


def test_factory():
    assert Factory.clone(foo=1).foo == 1


def test_factory_with_model_property():
    class Router(Factory):
        model = Artist

    assert Router.clone(model=Artist).__name__ == 'ArtistRouter'


def test_factory_with_model_argument():
    class Router(Factory):
        pass

    assert Router.clone(model=Artist).__name__ == 'ArtistRouter'
