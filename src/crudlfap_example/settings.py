from crudlfap.settings import *  # noqa

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS += [  # noqa
    # CRUDLFA+ extras
    'django_registration',
    'crudlfap_registration',

    # CRUDLFA+ examples
    'crudlfap_example.artist',
    'crudlfap_example.song',
    'crudlfap_example.blog',
]

ROOT_URLCONF = os.path.dirname(__file__).split('/')[-1] + '.urls'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', os.path.join(
            os.path.dirname(__file__),
            '..',
            'db.sqlite3',
        )),
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
