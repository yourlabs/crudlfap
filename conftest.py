import pytest
from django.contrib.sessions.backends.base import SessionBase
from django.test.client import RequestFactory as drf


class RequestFactory(drf):
    def __init__(self, user):
        self.user = user
        super().__init__()

    def generic(self, *args, **kwargs):
        request = super().generic(*args, **kwargs)
        request.session = SessionBase()
        request.user = self.user
        return request


@pytest.fixture
def srf():
    from django.contrib.auth.models import AnonymousUser
    return RequestFactory(AnonymousUser())
