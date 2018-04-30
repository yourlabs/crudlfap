"""
Hacked and meant to be imported in your project.

::

    from crudlfap.settings import *
    # [...] your settings
    install_optional(OPTIONAL_APPS, INSTALLED_APPS)
    install_optional(OPTIONAL_MIDDLEWARE, MIDDLEWARE)
"""


import os

from crudlfap.conf import install_optional  # noqa


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'notsecret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

if SECRET_KEY == 'notsecret' and not DEBUG:
    raise Exception('SECRET_KEY may not equal "notsecret" if not DEBUG')

if DEBUG and 'ALLOWED_HOSTS' not in os.environ:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Application definition
CRUDLFAP_APPS = [
    'crudlfap',
    'betterforms',
    'bootstrap3',
    'material',
    'crudlfap_filtertables2',
    'crudlfap_auth',
    'django_filters',
    'django_tables2',
    'django.contrib.admin',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + CRUDLFAP_APPS

# CRUDLFA+ optional dependencies
OPTIONAL_APPS = [
    # {'debug_toolbar': {'after': 'django.contrib.staticfiles'}},
    {'django_extensions': {'before': 'crudlfap'}},
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

OPTIONAL_MIDDLEWARE = [
    # {'debug_toolbar.middleware.DebugToolbarMiddleware': None}
]
INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'crudlfap_example.urls'

TEMPLATE_CONSTANTS = {
    "settings": dict(
        SITE_NAME='CRUDLFA+DEMO',
        SITE_TITLE='CRUDLFA+ demo !',
        DEBUG=DEBUG,
    ),
}

CRUDLFAP_TEMPLATE_BACKEND = {
    "BACKEND": "django_jinja.backend.Jinja2",
    "APP_DIRS": True,
    "OPTIONS": {
        "app_dirname": "jinja2",
        "match_extension": ".html",
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "django.template.context_processors.i18n",
        ],
        "extensions": [
            "jinja2.ext.do",
            "jinja2.ext.loopcontrols",
            "jinja2.ext.with_",
            "jinja2.ext.i18n",
            "jinja2.ext.autoescape",
            "django_jinja.builtins.extensions.CsrfExtension",
            "django_jinja.builtins.extensions.CacheExtension",
            "django_jinja.builtins.extensions.TimezoneExtension",
            "django_jinja.builtins.extensions.UrlsExtension",
            "django_jinja.builtins.extensions.StaticFilesExtension",
            "django_jinja.builtins.extensions.DjangoFiltersExtension",
        ],
        "constants": TEMPLATE_CONSTANTS,
        "globals": {
            "pagination_filter_params": "crudlfap.jinja2.pagination_filter_params",  # noqa
            "crudlfap_site": "crudlfap.crudlfap.site",
            "getattr": getattr,
            "str": str,
            "int": int,
            "isinstance": isinstance,
            "type": type,
            "render_table": "crudlfap_filtertables2.jinja2.render_table",
            "render_form": "crudlfap.jinja2.render_form",
            "render_button": "bootstrap3.forms.render_button",
            "json": "crudlfap.jinja2.json",
        },
        "newstyle_gettext": True,
        "bytecode_cache": {
            "name": "default",
            "backend": "django_jinja.cache.BytecodeCache",
            "enabled": False,
        },
        "autoescape": True,
        "auto_reload": DEBUG,
        "translation_engine": "django.utils.translation",
    }
}

try:
    import webpack_loader  # noqa
except ImportError:
    pass
else:
    CRUDLFAP_TEMPLATE_BACKEND['OPTIONS']['globals'].setdefault(
        'render_bundle',
        'webpack_loader.templatetags.webpack_loader.render_bundle',
    )

DEFAULT_TEMPLATE_BACKEND = {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
    },
}

TEMPLATES = [CRUDLFAP_TEMPLATE_BACKEND, DEFAULT_TEMPLATE_BACKEND]
LOGIN_REDIRECT_URL = '/'
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

WSGI_APPLICATION = 'crudlfap_example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
