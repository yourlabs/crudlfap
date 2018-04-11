from crudlfap import crudlfap

from django.urls import resolve, reverse

import pytest

from .crudlfap import User


@pytest.fixture
def user():
    return User.objects.get_or_create(username='foo')[0]


@pytest.mark.django_db
def test_get_menu(srf):
    srf.user = User.objects.create(is_superuser=True)
    result = crudlfap.site[User].get_menu('model', srf.get('/'))
    assert result[0].urlargs == []
    assert result[0].url == '/user/create'
    assert result[0].title == 'Create user'


def test_user_list_reverse():
    assert reverse('crudlfap:user:list') == '/user'


def test_user_create_reverse():
    assert reverse('crudlfap:user:create') == '/user/create'


def test_user_detail_reverse():
    assert reverse('crudlfap:user:detail', args=['a']) == '/user/a'


def test_user_delete_reverse():
    assert reverse('crudlfap:user:delete', args=['a']) == '/user/a/delete'


def test_user_update_reverse():
    assert reverse('crudlfap:user:update', args=['a']) == '/user/a/update'


@pytest.mark.django_db
def test_user_update_resolve(user):
    result = resolve('/user/foo/update')
    assert result.func.view_class.urlname == 'update'


def test_user_list_resolve():
    from crudlfap_filtertables2.views import FilterTables2ListView
    result = resolve('/user').func.view_class
    assert issubclass(result, FilterTables2ListView)
    assert result.__name__ == 'UserFilterTables2ListView'
    assert result.urlname == 'list'
    assert result.url == '/user'


def test_user_detail_url():
    view = crudlfap.site[User]['detail'](object=User(username='lol'))
    assert str(view.url) == '/user/lol'


def test_user_list_get(admin_client):
    result = admin_client.get('/user')
    assert result.status_code == 200


def test_user_create_get(admin_client):
    result = admin_client.get('/user/create')
    assert result.status_code == 200


@pytest.mark.django_db
def test_user_create_post(admin_client):
    result = admin_client.post('/user/create', dict(
        username='lol',
    ))
    assert result.status_code == 302
    assert result['Location'] == '/user/lol'


@pytest.mark.django_db
def test_user_create_post_with_next(admin_client):
    result = admin_client.post('/user/create', dict(
        username='lol',
        _next='/user',
    ))
    assert result.status_code == 302
    assert result['Location'] == '/user'


@pytest.mark.django_db
def test_user_detail_get(client, user):
    result = client.get('/user/foo')
    assert result.status_code == 302


@pytest.mark.django_db
def test_user_detail_get_admin(admin_client, user):
    result = admin_client.get('/user/foo')
    assert result.status_code == 200


@pytest.mark.django_db
def test_user_password_get(admin_client, user):
    result = admin_client.get('/user/foo/password')
    assert result.status_code == 200
    assert b'id_new_password2' in result.content
