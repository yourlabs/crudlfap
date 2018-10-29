"""
Test security with crudlfap_example.song setup.

It's a bit paranoid, but i'll sleep better with this: i don't trust users, i
don't trust myself either :)
"""
from datetime import timedelta

from crudlfap import crudlfap

from crudlfap_auth.crudlfap import User

from crudlfap_example.blog.models import Post

from django.utils import timezone

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


router = pytest.fixture(lambda: crudlfap.site[Post])
now = timezone.now()
yesterday = now - timedelta(days=1)
tomorrow = now + timedelta(days=1)

user0 = pytest.fixture(lambda: user(username='user0'))
user1 = pytest.fixture(lambda: user(username='user1'))
staff = pytest.fixture(lambda: user(username='staff', is_staff=True))

post0 = pytest.fixture(lambda user0: Post.objects.get_or_create(
    owner=user0, name='post0', publish=yesterday)[0])
post1 = pytest.fixture(lambda user0: Post.objects.get_or_create(
    owner=user0, name='post1', publish=tomorrow)[0])
post2 = pytest.fixture(lambda user1: Post.objects.get_or_create(
    owner=user1, name='post2', publish=yesterday)[0])

url = pytest.fixture(lambda name, obj: router()[name].clone(object=obj).url)


@pytest.mark.django_db
def test_list_view(router, client, user0, user1, post0, post1, post2):
    list_url = router['list'].url
    res = user_client(client, username='user0').get(list_url)
    assert b'post0' in res.content
    assert b'post1' in res.content
    assert b'post2' in res.content
    for name in ('update', 'delete'):
        view = router[name]
        assert str(view.clone(object=post0).url) in str(res.content)
        assert str(view.clone(object=post1).url) in str(res.content)
        assert str(view.clone(object=post2).url) not in str(res.content)

    res = user_client(client, username='user1').get(list_url)
    assert b'post0' in res.content
    assert b'post1' not in res.content
    assert b'post2' in res.content
    for name in ('update', 'delete'):
        view = router[name]
        assert str(view.clone(object=post0).url) not in str(res.content)
        assert str(view.clone(object=post1).url) not in str(res.content)
        assert str(view.clone(object=post2).url) in str(res.content)


@pytest.mark.django_db
def test_anonymous_detail_published(router, client, post0, post1):
    assert client.get(url('detail', post0)).status_code == 200
    assert client.get(url('detail', post1)).status_code == 404


@pytest.mark.django_db
def test_owner_detail_unpublished(router, client, post0, post1):
    client = user_client(client, username='user0')
    assert client.get(url('detail', post0)).status_code == 200
    assert client.get(url('detail', post1)).status_code == 200


@pytest.mark.django_db
def test_nonowner_detail_unpublished(router, client, post0, post1):
    client = user_client(client, username='user1')
    assert client.get(url('detail', post0)).status_code == 200
    assert client.get(url('detail', post1)).status_code == 404


@pytest.mark.parametrize('name', ['delete', 'update'])
@pytest.mark.django_db
def test_anonymous_edit_published(router, client, post0, post1, name):
    assert client.get(url(name, post0)).status_code == 404
    assert client.get(url(name, post1)).status_code == 404


@pytest.mark.parametrize('name', ['delete', 'update'])
@pytest.mark.django_db
def test_owner_edits(router, client, post0, post1, post2, name):
    client = user_client(client, username='user0')
    assert client.get(url(name, post0)).status_code == 200
    assert client.get(url(name, post1)).status_code == 200
    assert client.get(url(name, post2)).status_code == 404

    client = user_client(client, username='user1')
    assert client.get(url(name, post0)).status_code == 404
    assert client.get(url(name, post1)).status_code == 404
    assert client.get(url(name, post2)).status_code == 200
