from crudlfap.routers import Router
from crudlfap.test_routers import Artist
from crudlfap.utils import view_resolve

import pytest

urlpatterns = Router(Artist).urlpatterns()


@pytest.mark.urls('crudlfap.test_utils')
def test_view_resolve():
    view = view_resolve('artist_detail')
    assert view.get_slug() == 'detail'
    assert view.model == Artist
