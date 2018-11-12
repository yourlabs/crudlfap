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

AUTHENTICATION_BACKENDS += [  # noqa
    'crudlfap_example.blog.crudlfap.AuthBackend',
]
