from crudlfap.routers import Router

import pytest

from .urls import User


@pytest.fixture
def router():
    return Router.registry[User]


@pytest.fixture
def obj():
    return User(pk=1, username='bar')


def test_username_router(router, obj):
    view = router['detail'](object=obj)
    assert view.href == '/user/bar/'

    view = router['update'](object=obj)
    assert view.href == '/user/bar/update/'

    view = router['delete'](object=obj)
    assert view.href == '/user/bar/delete/'
