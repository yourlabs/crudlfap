def base(request):
    c = dict(base='base.html')
    base = request.POST.get('base', request.GET.get('base', False))

    if base in ('ajax', 'modal'):
        c['base'] = 'base_{}.html'.format(base)

    return c
