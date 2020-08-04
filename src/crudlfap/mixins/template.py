import logging

from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _

logger = logging.getLogger()


class TemplateMixin:
    """
    Replacement for Django's TemplateResponseMixin.

    This allows to configure "last resort" templates for each class, and thus
    to provide a working CRUD out of the box.
    """

    def get(self, request, *args, **kwargs):
        return self.render_to_response()

    def render_to_response(self):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        return self.response_class(
            request=self.request,
            template=self.template_names,
            context=self.context,
            using=self.template_engine,
            **self.response_kwargs
        )

    def get_template_engine(self):
        return 'crudlfap'

    def get_response_class(self):
        return TemplateResponse

    def get_response_kwargs(self):
        return dict(content_type='text/html')

    def get_context(self, **context):
        context['view'] = self
        self.context = context

    def get_view_label(self):
        return self.label

    def get_title(self):
        return _(self.view_label).capitalize()

    def get_title_link(self):
        """Return title attribute for links to this view."""
        return self.title

    def get_title_html(self):
        """Return text for HTML title tag."""
        return self.title

    def get_title_heading(self):
        """Return text for page heading."""
        return self.title

    def get_template_name_suffix(self):
        return '_' + self.urlname

    def get_template_names(self):
        """Give a chance to default_template_name."""
        template_names = []
        template_name = getattr(self, 'template_name', None)
        if template_name:
            template_names.append(template_name)

        if getattr(self, 'model', None):
            template_names.append('%s/%s%s.html' % (
                self.model._meta.app_label,
                self.model._meta.model_name,
                self.template_name_suffix
            ))

        default_template_name = getattr(self, 'default_template_name', None)
        if default_template_name:
            template_names.append(default_template_name)
        logger.debug('TEMPLATE_NAMES', template_names)
        return template_names
