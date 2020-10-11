import copy
import urllib

from django import template
from django.utils.safestring import mark_safe


def pagination_filter_params(data):
    data = copy.deepcopy(data)
    if 'page' in data:
        data.pop('page')
    return urllib.parse.urlencode(data)


def render_form(form):
    from ryzom.components.muicss import Form
    return mark_safe(Form(form).to_html())
