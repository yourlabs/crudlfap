from django.template.context import RequestContext
from django.template.loader import get_template
from django.template import Template

def render_table(request, table, object_list):
    """Poor man's binding to Django render_table template tag."""
    context = RequestContext(request, dict(
        table=table,
        object_list=object_list
    ))
    template = Template('''
    {% load django_tables2 %}{% render_table table %}
    ''')
    html = template.render(context)
    return html
