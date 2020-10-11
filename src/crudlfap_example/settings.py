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


RYZOM_TEMPLATE_BACKEND = {
    "BACKEND": "ryzom.backends.ryzom.Ryzom",
    "OPTIONS": {
        "app_dirname": "components",
        "components_module": "ryzom.components.muicss",
        "components_prefix": "Mui",
        # "components_module": "ryzom.components.django",
        # "components_prefix": "Django",

        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "django.template.context_processors.i18n",
        ],
        # "autoescape": True,
        # "auto_reload": DEBUG,
        # "translation_engine": "django.utils.translation",
        # "debug": False,
    }
}
TEMPLATES.append(RYZOM_TEMPLATE_BACKEND)

