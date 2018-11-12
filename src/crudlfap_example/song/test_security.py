"""
Test security with crudlfap_example.song setup.

It's a bit paranoid, but i'll sleep better with this: i don't trust users, i
don't trust myself either :)
"""

from crudlfap import shortcuts as crudlfap

from crudlfap_auth.crudlfap import User

from crudlfap_example.artist.models import Artist
from crudlfap_example.song.models import Song

import pytest


def user(**attrs):
    user, created = User.objects.get_or_create(**attrs)
    if created:
        user.set_password('password')
        user.save()
    return user


def user_client(client, **userattrs):
    if not userattrs.get('username', None):
        return client
    user(**userattrs)
    if not client.login(username=userattrs['username'], password='password'):
        raise Exception('Could not auth as ' + userattrs['username'])
    return client


@pytest.fixture
def song0():
    user0 = user(username='user0')
    artist = Artist.objects.get_or_create(name='artist0')[0]
    return Song.objects.get_or_create(
        artist=artist, name='song0', owner=user0)[0]


cases = [
    (dict(), False),
    (dict(username='user0'), True),
    (dict(username='user1'), False),
    (dict(username='staff', is_staff=True), True),
    (dict(username='superuser', is_superuser=True), True),
]


@pytest.mark.parametrize('userattrs,expected', cases)
@pytest.mark.parametrize('url', ['detail', 'update', 'delete'])
@pytest.mark.django_db
def test_object_views_object_for_user(client, userattrs, expected, url, song0):
    view = crudlfap.site[Song][url].clone(object=song0)
    url = view.url
    res = user_client(client, **userattrs).get(url)
    assert res.status_code == 200 if expected else 404


@pytest.mark.parametrize('userattrs,expected', cases)
@pytest.mark.django_db
def test_list_view_get_objects_for_user(client, userattrs, expected, song0):
    res = user_client(client, **userattrs).get(crudlfap.site[Song]['list'].url)

    assert res.status_code == 200 if userattrs else 302

    if expected:
        assert b'song0' in res.content
    else:
        assert b'song0' not in res.content
