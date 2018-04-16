from django.core.exceptions import FieldDoesNotExist


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
