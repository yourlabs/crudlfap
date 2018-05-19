import copy
import urllib

from django import template
from django.template.context import RequestContext


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


def render_table(request, table, object_list):
    """Poor man's binding to Django render_table template tag."""
    context = RequestContext(request, dict(
        table=table,
        object_list=object_list
    ))
    t = template.Template('''
    {% load django_tables2 %}{% render_table table %}
    ''')
    html = t.render(context)
    return html
