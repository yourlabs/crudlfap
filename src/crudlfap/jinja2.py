import copy
import urllib

from django.template import Context
from django.template.loader import select_template



def render_django_template(template_name_list, **context):
    return select_template(template_name_list).render(Context(context))


def pagination_filter_params(data):
    data = copy.deepcopy(data)
    if 'page' in data:
        data.pop('page')
    return urllib.parse.urlencode(data)


def link(url_name, html, attributes=None):
    pass


def get_view(url_name):
    pass
