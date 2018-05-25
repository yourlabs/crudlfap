from django import http


class FormMixin:
    """Mixin for views which have a Form."""

    success_url_next = True
    initial = {}
    success_url = None

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        return http.HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
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

    def get_form(self):
        """Return an instance of the form to be used in this view."""
        import ipdb; ipdb.set_trace()
        return self.form_class(**self.get_form_kwargs())
    get_form.autoset = True

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        if self.success_url_next and '_next' in self.request.POST:
            return self.request.POST['_next']
        if self.object and hasattr(self.object, 'get_absolute_url'):
            return self.object.get_absolute_url()
        if self.router['list']:
            return self.router['list'].url
        return super().get_success_url()
