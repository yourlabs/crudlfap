import copy
import urllib

from django import template


def pagination_filter_params(data):
    data = copy.deepcopy(data)
    if 'page' in data:
        data.pop('page')
    return urllib.parse.urlencode(data)


def render_form(form):
    tpl = ['{% load material_form %}{% form form=form ']
    context = dict(form=form)

    if getattr(form, '_layout', None):
        tpl.append('layout=layout')
        context['layout'] = form._layout

    tpl.append('%}{% endform %}')

    return template.Template(
        ' '.join(tpl)
    ).render(template.Context(context))
