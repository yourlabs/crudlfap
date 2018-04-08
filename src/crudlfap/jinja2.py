import copy
import urllib

from django import template


def pagination_filter_params(data):
    data = copy.deepcopy(data)
    if 'page' in data:
        data.pop('page')
    return urllib.parse.urlencode(data)


def link(url_name, html, attributes=None):
    pass


def get_view(url_name):
    pass


def json(arg):
    import json
    return json.dumps(arg)


def render_form(form):
    return template.Template(
        '{% load material_form %}{% form form=form %}{% endform %}'
    ).render(template.Context(dict(form=form)))
