from jinja2.ext import Extension


def base(request):
    c = dict(base='base.html')

    if request.is_ajax() or request.GET.get('is_ajax', False):
        c['base'] = 'base_modal.html'

    return c
