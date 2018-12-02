from crudlfap import crudlfap

from django.contrib.auth.models import Group, Permission
from django.urls import resolve, reverse

import pytest

from .crudlfap import User


@pytest.fixture
def user():
    return User.objects.get_or_create(username='foo')[0]


@pytest.fixture
def suuser():
    return User.objects.create_superuser(
        username='suuser', password='123', email='')


@pytest.fixture
def group():
    return Group.objects.get_or_create(name='1')[0]


@pytest.mark.django_db
def test_get_menu(srf):
    srf.user = User.objects.create(is_superuser=True)
    result = crudlfap.site[User].get_menu('model', srf.get('/'))
    assert result[0].urlargs == []
    assert result[0].url == '/user/create'
    assert result[0].title == 'User: create'


def test_user_list_reverse():
    assert reverse('crudlfap:user:list') == '/user'


def test_user_create_reverse():
    assert reverse('crudlfap:user:create') == '/user/create'


def test_user_deleteobjects_reverse():
    assert reverse('crudlfap:user:deleteobjects') == '/user/deleteobjects'


def test_user_detail_reverse():
    assert reverse('crudlfap:user:detail', args=['a']) == '/user/a'


def test_user_delete_reverse():
    assert reverse('crudlfap:user:delete', args=['a']) == '/user/a/delete'


def test_user_update_reverse():
    assert reverse('crudlfap:user:update', args=['a']) == '/user/a/update'


def test_group_list_reverse():
    assert reverse('crudlfap:group:list') == '/group'


def test_group_create_reverse():
    assert reverse('crudlfap:group:create') == '/group/create'


def test_group_detail_reverse():
    assert reverse('crudlfap:group:detail', args=['1']) == '/group/1'


def test_group_delete_reverse():
    assert reverse('crudlfap:group:delete', args=['1']) == '/group/1/delete'


def test_group_update_reverse():
    assert reverse('crudlfap:group:update', args=['1']) == '/group/1/update'


def test_su_user_reverse():
    assert reverse('crudlfap:su') == '/su'


def test_login_reverse():
    assert reverse('crudlfap:login') == '/login'


def test_logout_reverse():
    assert reverse('crudlfap:logout') == '/logout'


def test_url_reverse():
    assert reverse('crudlfap:urls') == '/urls'


@pytest.mark.django_db
def test_user_update_resolve(user):
    result = resolve('/user/foo/update')
    assert result.func.view_class.urlname == 'update'


@pytest.mark.django_db
def test_user_delete_resolve(user):
    result = resolve('/user/foo/delete')
    assert result.func.view_class.urlname == 'delete'


@pytest.mark.django_db
def test_user_deleteobjects_resolve(user):
    result = resolve('/user/deleteobjects')
    assert result.func.view_class.urlname == 'deleteobjects'


@pytest.mark.django_db
def test_user_create_resolve(user):
    result = resolve('/user/create')
    assert result.func.view_class.urlname == 'create'


@pytest.mark.django_db
def test_user_detail_resolve(user):
    result = resolve('/user/foo')
    assert result.func.view_class.urlname == 'detail'


@pytest.mark.django_db
def test_user_logout_resolve(user):
    result = resolve('/logout')
    assert result.func.view_class.urlname == 'logout'


@pytest.mark.django_db
def test_user_login_resolve():
    result = resolve('/login')
    assert result.func.view_class.urlname == 'login'


def test_user_list_resolve():
    result = resolve('/user').func.view_class
    assert issubclass(result, crudlfap.ListView)
    assert result.__name__ == 'UserListView'
    assert result.urlname == 'list'
    assert result.url == '/user'


def test_group_list_resolve():
    result = resolve('/group').func.view_class
    assert issubclass(result, crudlfap.ListView)
    assert result.__name__ == 'GroupListView'
    assert result.urlname == 'list'
    assert result.url == '/group'


@pytest.mark.django_db
def test_group_update_resolve(group):
    result = resolve('/group/1/update')
    assert result.func.view_class.urlname == 'update'


@pytest.mark.django_db
def test_group_delete_resolve(group):
    result = resolve('/group/1/delete')
    assert result.func.view_class.urlname == 'delete'


@pytest.mark.django_db
def test_group_create_resolve(group):
    result = resolve('/group/create')
    assert result.func.view_class.urlname == 'create'


@pytest.mark.django_db
def test_group_detail_resolve(group):
    result = resolve('/group/1')
    assert result.func.view_class.urlname == 'detail'


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
def test_user_deleteobjects_get(admin_client):
    for i in range(100, 103):
        User.objects.get_or_create(pk=i, username='user{}'.format(i))
    result = admin_client.get('/user/deleteobjects?pks=101&pks=102')
    assert result.status_code == 200


def test_group_list_get(admin_client):
    result = admin_client.get('/group')
    assert result.status_code == 200


def test_group_create_get(admin_client):
    result = admin_client.get('/group/create')
    assert result.status_code == 200


@pytest.mark.django_db
def test_group_create_post(admin_client):
    result = admin_client.post('/group/create', dict(
        name='1',
    ))
    assert result.status_code == 302
    assert result['Location'] == '/group/1'


@pytest.mark.django_db
def test_group_create_post_with_permission(admin_client):
    permission = Permission.objects.filter().first()
    result = admin_client.post('/group/create', dict(
        name='1',
        permissions=permission.id
    ))
    assert result.status_code == 302
    assert result['Location'] == '/group/1'


@pytest.mark.django_db
def test_group_update_post(admin_client, group):
    permission = Permission.objects.filter().first()
    result = admin_client.post('/group/1/update', dict(
        name='1',
        permissions=permission.id
    ))
    assert result.status_code == 302
    assert result['Location'] == '/group/1'


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
        password='Download@123',
        _next='/user',
    ))
    assert result.status_code == 302
    assert result['Location'] == '/user'


@pytest.mark.django_db
def test_user_password_post(admin_client, user):
    result = admin_client.post('/user/foo/password', dict(
        old_password='Download@123',
        new_password1='Download123',
        new_password2='Download123',
    ))
    assert result.status_code == 302
    assert result['Location'] == '/user/foo'


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


@pytest.mark.django_db
def test_group_detail_get(admin_client, group):
    result = admin_client.get('/group/1')
    assert result.status_code == 200


@pytest.mark.django_db
def test_group_delete(admin_client):
    result = admin_client.get('/group/1/delete', dict(
        _next='/user',
    ))
    assert result.status_code == 404


@pytest.mark.django_db
def test_user_login_get(admin_client):
    result = admin_client.get('/login')
    assert result.status_code == 302


@pytest.mark.django_db
def test_user_login_post(admin_client):
    result = admin_client.post('/login', dict(
        username='lol',
        new_password1='123',
    ))
    assert result.status_code == 302
    assert result['Location'] == '/'


@pytest.mark.django_db
def test_user_logout_get(admin_client):
    result = admin_client.get('/logout')
    assert result.status_code == 200


def test_become_user(admin_client, admin_user, suuser, user):
    assert admin_client.session.get('become_user') is None

    result = admin_client.get('/user/admin/su', follow=True)
    assert result.status_code == 200
    assert admin_client.session.get('become_user') == admin_user.id

    result = admin_client.get('/user/suuser/su', follow=True)
    assert result.status_code == 200
    assert admin_client.session.get('become_user') == admin_user.id

    result = admin_client.get('/su', follow=True)
    assert result.status_code == 200
    assert admin_client.session.get('become_user') is None

    result = admin_client.get('/user/foo/su', follow=True)
    assert result.status_code == 200
