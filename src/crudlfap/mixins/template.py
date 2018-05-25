

class TemplateMixin(object):
    """
    Override for get_template_names to append default_template_name.

    This allows to configure "last resort" templates for each class, and thus
    to provide a working CRUD out of the box.
    """

    style = 'default'
    fa_icon = 'question'
    material_icon = 'priority high'
    ajax = '#ajax-container'

    def get_view_label(self):
        return self.label

    def get_title(self):
        return _(self.view_label).capitalize()

    def get_title_menu(self):
        """Return title for menu links to this view."""
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

    def get_template_names(self):
        """Give a chance to default_template_name."""
        default_template_name = getattr(self, 'default_template_name', None)

        try:
            template_names = super().get_template_names()
        except ImproperlyConfigured:
            if not default_template_name:
                raise
            template_names = []

        if default_template_name:
            template_names.append(default_template_name)
        return template_names
