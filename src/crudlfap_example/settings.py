from crudlfap.settings import *  # noqa

INSTALLED_APPS += [  # noqa
    # CRUDLFA+ examples
    'crudlfap_example.artist',
    'crudlfap_example.song',
    'crudlfap_example.nondb',
    'crudlfap_example.blog',
]

install_optional(OPTIONAL_APPS, INSTALLED_APPS)  # noqa
install_optional(OPTIONAL_MIDDLEWARE, MIDDLEWARE)  # noqa


# SAUCE_LAB

USERNAME = 'jpic'
KEY = '626cba16-37e5-4ff8-8fc2-4df389fa7c29'
PASSWORD = 'iequaethoo3shobei3jukaineil2eTh0'

