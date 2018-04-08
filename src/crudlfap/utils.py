from django.core.exceptions import FieldDoesNotExist
from django.urls.base import get_resolver, get_urlconf


def view_resolve(url_name, urlconf=None):
    if urlconf is None:
        urlconf = get_urlconf()

    resolver = get_resolver(urlconf)

    for url in resolver.url_patterns:
        if url.name == url_name:
            return url.callback.view_class


def guess_urlfield(model):
    if not model:
        return None

    try:
        model._meta.get_field('slug')
    except FieldDoesNotExist:
        pass
    else:
        return 'slug'

    return 'pk'
