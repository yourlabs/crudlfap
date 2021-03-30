from .conf import install_optional


def get_installed():
    return ['django.contrib.staticfiles', 'crudlfap', 'myapp'].copy()


def test_install_optional():
    bs3 = {'debug_toolbar': {'after': 'django.contrib.staticfiles'}}
    messages = {
        'django.contrib.messages': {
            'before': 'django.contrib.staticfiles'
        }
    }
    nonexistent = {
        'nonexistent': None,
    }
    ctx = {
        'crudlfap_auth': None,
    }
    after = get_installed()
    install_optional([bs3], after)
    expect = [
        'django.contrib.staticfiles',
        'debug_toolbar',
        'crudlfap',
        'myapp',
    ]
    assert after == expect, "Failed to insert bootstrap3 after crudlfap"
    before_and_after = get_installed()
    install_optional([bs3, messages], before_and_after)
    expected = ['django.contrib.messages', 'django.contrib.staticfiles',
                'debug_toolbar', 'crudlfap', 'myapp']
    assert before_and_after == expected, "Failed before and after"
    nono = get_installed()
    install_optional([nonexistent], nono)
    assert nono == get_installed(), "Non existing app installed"
    mod_attr = get_installed()
    install_optional([ctx], mod_attr)
    expected = ['django.contrib.staticfiles', 'crudlfap', 'myapp',
                'crudlfap_auth']
    assert mod_attr == expected, "Failed to append module attribute reference"
