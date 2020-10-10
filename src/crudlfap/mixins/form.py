from django import http
from django.contrib import messages


class FormMixin:
    """Mixin for views which have a Form."""

    success_url_next = True
    initial = {}
    default_template_name = 'crudlfap/form.html'

    def get_context(self, **context):
        context['form'] = self.form
        return super().get_context(**context)

    def form_valid(self):
        """If the form is valid, redirect to the supplied URL."""
        self.message_success()
        return http.HttpResponseRedirect(self.success_url)

    def form_invalid(self):
        """If the form is invalid, render the invalid form."""
        self.message_error()
        return self.render_to_response()

    def get_title_submit(self):
        """
        Title of the submit button.

        Defaults to :py:attr:`~crudlfap.mixins.menu.MenuMixin.title_menu`
        """
        return self.title_menu

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        if self.form.is_valid():
            return self.form_valid()
        else:
            return self.form_invalid()

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return None

    def get_form_class(self):
        if self.router:
            return getattr(self.router, 'form_class')

    def get_form(self):
        """Return an instance of the form to be used in this view."""
        self.form = self.form_class(**self.get_form_kwargs())
        return self.form

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        self.form_kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            self.form_kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return self.form_kwargs

    def get_next_url(self):
        if '_next' in self.request.POST:
            self.next_url = self.request.POST.get('_next')
        if '_next' in self.request.GET:
            self.next_url = self.request.GET.get('_next')

    def get_success_url(self):
        if self.next_url:
            return self.next_url

        if (hasattr(self, 'object')
                and hasattr(self.object, 'get_absolute_url')):
            return self.object.get_absolute_url()

        if self.router['list']:
            return self.router['list'].url

        return super().get_success_url()

    def message_html(self, message):
        return message

    def message_success(self):
        messages.success(
            self.request,
            self.message_html(self.form_valid_message)
        )

    def message_error(self):
        messages.error(
            self.request,
            self.message_html(self.form_invalid_message)
        )
