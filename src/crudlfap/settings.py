"""
Hacked and meant to be imported in your project.

::

    from crudlfap.settings import autosettings
    # [...] your settings, see crudlfap_example/settings.py
    autosettings(globals())
"""

import copy
import os

from crudlfap.conf import install_optional

# CRUDLFA+ optional dependencies
CRUDLFAP_OPTIONAL_APPS = [
    {'debug_toolbar': {'after': 'django.contrib.staticfiles'}},
    {'crudlfap_filtertables2': {'after': 'crudlfap'}},
    {'django_filters': {'after': 'crudlfap'}},
    {'django_tables2': {'after': 'crudlfap'}},
    {'dal': {'before': 'crudlfap'}},
    {'dal_select2': {'before': 'crudlfap'}},
]

CRUDLFAP_OPTIONAL_MIDDLEWARE = [
    {'debug_toolbar.middleware.DebugToolbarMiddleware': None}
]

TEMPLATE_CONSTANTS = {
    'settings': dict(
        SITE_NAME='CRUDLFA+DEMO',
        SITE_TITLE='CRUDLFA+ demo !',
    ),
}

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.i18n',
]

CRUDLFAP_TEMPLATE_BACKEND = {
    'BACKEND': 'django_jinja.backend.Jinja2',
    'APP_DIRS': True,
    'OPTIONS': {
        'app_dirname': 'jinja2',
        'match_extension': '.html',
        'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        'extensions': [
            'jinja2.ext.do',
            'jinja2.ext.loopcontrols',
            'jinja2.ext.with_',
            'jinja2.ext.i18n',
            'jinja2.ext.autoescape',
            'django_jinja.builtins.extensions.CsrfExtension',
            'django_jinja.builtins.extensions.CacheExtension',
            'django_jinja.builtins.extensions.TimezoneExtension',
            'django_jinja.builtins.extensions.UrlsExtension',
            'django_jinja.builtins.extensions.StaticFilesExtension',
            'django_jinja.builtins.extensions.DjangoFiltersExtension',
        ],
        'constants': TEMPLATE_CONSTANTS,
        'globals': {
            'pagination_filter_params': 'crudlfap.jinja2.pagination_filter_params',  # noqa
            'Router': 'crudlfap.routers.Router',
            'render_bundle': 'crudlfap.jinja2.render_bundle',
            'getattr': getattr,
            'str': str,
            'int': int,
            'isinstance': isinstance,
            'type': type,
            'select_template': 'django.template.loader.select_template',
            'Context': 'django.template.Context',
            'Template': 'django.template.Template',
            'render_table': 'crudlfap_filtertables2.jinja2.render_table',
            'render_form': 'bootstrap3.forms.render_form',
            'render_button': 'bootstrap3.forms.render_button',
        },
        'newstyle_gettext': True,
        'bytecode_cache': {
            'name': 'default',
            'backend': 'django_jinja.cache.BytecodeCache',
            'enabled': False,
        },
        'autoescape': True,
        'translation_engine': 'django.utils.translation',
    }
}

DEFAULT_TEMPLATE_BACKEND = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
    },
}

TEMPLATES = [CRUDLFAP_TEMPLATE_BACKEND, DEFAULT_TEMPLATE_BACKEND]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.{}'.format(n),
    } for n in [
        'UserAttributeSimilarityValidator',
        'MinimumLengthValidator',
        'CommonPasswordValidator',
        'NumericPasswordValidator',
    ]
]

REQUIRED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'material',
    'crudlfap',
    'webpack_loader' if shutil.which('npm') else 'webpack_mock',
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


# Copyright Ferry Boender, released under the MIT license.
def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in src.items():
        if type(v) == list:
            if k not in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if k not in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if k not in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)


def autologger(g):
    if os.getenv('LOG'):
        g.setdefault(
            'LOGGING',
            {
                'version': 1,
                'disable_existing_loggers': False,
                'handlers': {
                    'console': {
                        'level': 'INFO',
                        'class': 'logging.StreamHandler',
                        'formatter': 'simple'
                    },
                    'file.error': {
                        'level': 'ERROR',
                        'class': 'logging.FileHandler',
                        'filename': os.path.join(
                            os.getenv('LOG'),
                            'django.error.log',
                        ),
                        'formatter': 'simple',
                    },
                    'file.info': {
                        'level': 'INFO',
                        'class': 'logging.FileHandler',
                        'filename': os.path.join(
                            os.getenv('LOG'),
                            'django.info.log',
                        ),
                        'formatter': 'simple'
                    },
                    'file.debug': {
                        'level': 'DEBUG',
                        'class': 'logging.FileHandler',
                        'filename': os.path.join(
                            os.getenv('LOG'),
                            'django.debug.log',
                        ),
                        'formatter': 'simple'
                    },
                },
                'formatters': {
                    'simple': {
                        'format': '%(levelname)s %(name)s %(message)s'
                    },
                },
                'loggers': {
                    'django': {
                        'handlers': [
                            'file.error',
                            'file.info',
                            'file.debug',
                            'console'
                        ],
                        'level': 'DEBUG' if g['DEBUG'] else 'INFO',
                        'propagate': True,
                    },
                },
            }
        )
    else:
        g.setdefault(
            'LOGIN_REDIRECT_URL',
            {
                'version': 1,
                'disable_existing_loggers': False,
                'handlers': {
                    'console': {
                        'level': 'INFO',
                        'class': 'logging.StreamHandler',
                        'formatter': 'simple'
                    },
                },
                'formatters': {
                    'simple': {
                        'format': '%(levelname)s %(message)s'
                    },
                },
                'loggers': {
                    '*': {
                        'handlers': ['console'],
                        'level': 'INFO',
                        'propagate': True,
                    },
                },
            }
        )


def basedir(basefile, *args):
    return os.path.abspath(
        os.path.join(
            os.path.dirname(basefile),
            *args
        )
    )


def settings(g, name, default):
    if name not in g:
        g[name] = default
        print('    {}={}'.format(name, default))


def autosettings(g, write):  # noqa
    def setting(name, default):
        return settings(g, name, default)

    settings_module = os.getenv('DJANGO_SETTINGS_MODULE')
    # print('autosettings({})'.format(settings_module))

    mod = settings_module.split('.')[0]

    for app in REQUIRED_APPS:
        if app not in g['INSTALLED_APPS']:
            # print('    INSTALLED_APPS insert: {}'.format(app))
            g['INSTALLED_APPS'].insert(0, app)

    # Set DEBUG to False by default, the crudlfap.manage.main endpoint enables
    # it by default. This prevents wsgi.py to have it enabled by default and
    # prevents DEBUG from being enabled by default in production.
    setting('DEBUG', os.getenv('DEBUG', False))

    # Disabling DEBUG requires setting a secret key, to circumvent export:
    # SECRET_KEY='debug' DEBUG=
    if not g['DEBUG'] and 'SECRET_KEY' not in os.environ:
        raise Exception('$SECRET_KEY is required if DEBUG is False')
    setting('SECRET_KEY', os.getenv('SECRET_KEY', 'debug'))

    # Disabling DEBUG requires setting a secret key, to circumvent export:
    # SECRET_KEY='debug' ALLOWED_HOSTS='*' DEBUG=
    if not g['DEBUG'] and 'ALLOWED_HOSTS' not in os.environ:
        raise Exception('$ALLOWED_HOSTS is required if DEBUG is False')
    setting('ALLOWED_HOSTS', [])

    if 'ALLOWED_HOSTS' in os.environ:
        hosts = os.getenv('ALLOWED_HOSTS')
        g['ALLOWED_HOSTS'].append(hosts)
        # print('    ALLOWED_HOSTS add: {}'.format(hosts))

    setting('INTERNAL_IPS', ('127.0.0.1',))
    setting('STATIC_URL', '/static/')
    setting('STATIC_ROOT', os.path.join(write, 'static'))
    setting('STATICFILES_DIRS', [])
    setting('MEDIA_URL', '/media/')
    setting('MEDIA_ROOT', os.path.join(write, 'media'))
    g.setdefault('MIDDLEWARE', MIDDLEWARE)
    if not g['DEBUG'] and 'AUTH_PASSWORD_VALIDATORS' not in g:
        setting('AUTH_PASSWORD_VALIDATORS', AUTH_PASSWORD_VALIDATORS)

    if 'TEMPLATE_CONSTANTS' in g:
        deepupdate(g['TEMPLATE_CONSTANTS'], TEMPLATE_CONSTANTS)
        # print('    TEMPLATE_CONSTANTS={}'.format(g['TEMPLATE_CONSTANTS']))

    g.setdefault(
        'DATABASES',
        {
            'default': {
                'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
                'NAME': os.getenv(
                    'DB_NAME',
                    os.path.join(write, 'db.sqlite3')
                ),
                'USER': os.getenv('DB_USER', None),
                'PASSWORD': os.getenv('DB_PASSWORD', None),
                'HOST': os.getenv('DB_HOST', None),
                'PORT': os.getenv('DB_PORT', None),
            }
        }
    )
    dbs = copy.deepcopy(g['DATABASES'])
    for db in dbs.values():
        db.pop('PASSWORD')
    # print('    DATABASES={}'.format(g['DATABASES']))

    CRUDLFAP_TEMPLATE_BACKEND['OPTIONS'].setdefault('auto_reload', g['DEBUG'])
    setting('TEMPLATES', TEMPLATES)
    setting('ROOT_URLCONF', '{}.urls'.format(mod))
    setting('WSGI_APPLICATION', '{}.wsgi.application'.format(mod))
    setting('LOGIN_REDIRECT_URL', '/')

    setting('EMAIL_HOST', os.getenv('EMAIL_HOST', None))
    setting('EMAIL_PORT', os.getenv('EMAIL_PORT', None))
    setting('EMAIL_HOST_USER', os.getenv('EMAIL_HOST_USER', None))
    # if 'EMAIL_HOST_PASSWORD' in os.environ:
    # print('    EMAIL_HOST_PASSWORD=****')
    g.setdefault('EMAIL_HOST_PASSWORD', os.getenv('EMAIL_HOST_PASSWORD', None))
    setting('EMAIL_USE_TLS', os.getenv('EMAIL_USE_TLS', None))
    setting('EMAIL_USE_SSL', os.getenv('EMAIL_USE_SSL', None))

    if g['DEBUG']:
        g.setdefault(
            'EMAIL_BACKEND',
            os.getenv(
                'EMAIL_BACKEND',
                'django.core.mail.backends.console.EmailBackend'
            )
        )
    else:
        g.setdefault(
            'EMAIL_BACKEND',
            os.getenv(
                'EMAIL_BACKEND',
                'django.core.mail.backends.smtp.EmailBackend',
            )
        )

    if 'OPTIONAL_APPS' in g:
        install_optional(g['OPTIONAL_APPS'], g['INSTALLED_APPS'])
    if 'OPTIONAL_MIDDLEWARE' in g:
        install_optional(g['OPTIONAL_MIDDLEWARE'], g['MIDDLEWARE'])

    autologger(g)

    install_optional(CRUDLFAP_OPTIONAL_APPS, g['INSTALLED_APPS'])
    install_optional(CRUDLFAP_OPTIONAL_MIDDLEWARE, g['MIDDLEWARE'])

    # print('    INSTALLED_APPS={}'.format(g['INSTALLED_APPS']))
    # print('    MIDDLEWARE={}'.format(g['MIDDLEWARE']))

    return g
