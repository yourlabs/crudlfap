from crudlfap.settings import *  # noqa

INSTALLED_APPS += [  # noqa
    # CRUDLFA+ examples
    'crudlfap_example.artist',
    'crudlfap_example.song',
    'crudlfap_example.blog',

    # CRUDLFA+ extras
    'django_registration',
    'crudlfap_registration',
]

ROOT_URLCONF = 'crudlfap_example.urls'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'HOST': os.getenv('DB_HOST'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
    }
}

install_optional(OPTIONAL_APPS, INSTALLED_APPS)  # noqa
install_optional(OPTIONAL_MIDDLEWARE, MIDDLEWARE)  # noqa

AUTHENTICATION_BACKENDS += [  # noqa
    'crudlfap_example.blog.crudlfap.AuthBackend',
]
