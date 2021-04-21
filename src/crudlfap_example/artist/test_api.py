import json
import pytest

from crudlfap_auth.crudlfap import User


@pytest.mark.django_db
def test_api(client):
    user = User.objects.create(is_superuser=True, is_active=True)
    client.force_login(user)

    # test valid form
    response = client.post(
        '/artist/create',
        json.dumps(dict(
            name='test artist',
        )),
        content_type='application/json'
    )
    assert response.status_code == 201

    # test invalid form
    response = client.post(
        '/artist/create',
        json.dumps(dict(
            name='',
        )),
        content_type='application/json'
    )
    assert response.status_code == 405

    # test list get
    response = client.get(
        '/artist',
        HTTP_ACCEPT='application/json',
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == 1
    assert data['results'][0]['name'] == 'test artist'
    response = client.get(
        f'/artist/{data["results"][0]["id"]}',
        HTTP_ACCEPT='application/json'
    )
    assert response.json() == {'id': 1, 'name': 'test artist'}
