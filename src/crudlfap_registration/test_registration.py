import pytest
import re


@pytest.mark.django_db
def test_registration(client, mailoutbox):
    assert len(mailoutbox) == 0
    response = client.post('/registration/register/', dict(
        email='testregistration@example.com',
        username='testregistration',
        password1='!@aoe@#$',
        password2='!@aoe@#$',
    ))
    assert response.status_code == 302
    assert len(mailoutbox) == 1
    match = re.search('http://testserver[^\n]*', mailoutbox[0].body)
    assert match
    activate = match.group()
    response = client.get(activate)
    assert response.status_code == 302
    assert response['Location'] == '/registration/activate/complete/'
    response = client.post('/auth/login/', dict(
        username='testregistration',
        password='!@aoe@#$',
    ))
    assert response.status_code == 302
