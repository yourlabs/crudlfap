"""Sets the default appconfig to :py:cls:`~crudlfap.apps.DefaultConfig`."""
from django.utils.module_loading import autodiscover_modules


def autodiscover():
    autodiscover_modules('crudlfap')


default_app_config = 'crudlfap.apps.DefaultConfig'
