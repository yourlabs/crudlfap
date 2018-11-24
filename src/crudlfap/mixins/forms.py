from django import http
from django.contrib import messages


class FormsMixin:
    """
    Mixin for views which have forms.

    The only required attribute is
    :py:attr:`forms_classes` which is expected to be a
    dict of prefix: FormClass, ie.::

        class YourObjectUpdate(crudlfap.FormsMixin, crudlfap.UpdateView):
            forms_classes = dict(
                person=PersonForm,
            )

    Then, :py:attr:`forms_initial` for example is expected
    to be a dict of prefixes as key names and initial
    value for the corresponding form.

    However, the default :py:meth:`get_forms_initial`
    implementation will try to call the
    get_prefixname_initial method by default for each
    prefix in :py:attr:`form_classes`.

    In case of attribute error it will fallback
    to the :py:attr:`forms_initial_default` attribute that
    you can also set, or override the default
    :py:meth:`get_forms_initial_default` implementation.

    .. py:attribute:: forms_classes

        You should set this to a dict of prefix: FormClass.

    .. py:attribute:: forms_initial

        Expected to be a dict of prefix: {} by default.

    Note that this is compatible with views that use the
    FormMixin, at the condition that FormsMixin is before
    in the MRO of course. In this case, you will deal with both self.form from FormMixin and self.forms from FormsMixin in your form_valid()
    """

    def get_success_url_next(self):
        """Returns True by default, to enable following next GET attribute."""
        return True

    def get_default_template_name(self):
        """Return the ``crudlfap/form.html`` template by default."""
        return 'crudlfap/form.html'

    def get_forms_configuration(self, name):
        """
        Return a dict of prefix: config for each form.

        Relies on the :py:meth:`get_forms_default` method.
        """
        return {
            prefix: self.get_forms_default(name, prefix)
            for prefix in self.forms_classes.keys()
        }

    def get_forms_default(self, name, prefix):
        """Attribute tryer for a variable for a form prefix.

        It will return `self.forms_{name}_{prefix}` or
        `self.forms_{name}_default` in case of
        AttributeError, ie. `self.forms_initial_default`
        will be returned if returning
        `self.forms_initial_person` raised an
        AttributeError.
        """
        try:
            return getattr(self, f'forms_{name}_{prefix}')
        except AttributeError:
            return getattr(self, f'forms_{name}_default')

    def get_forms_initial(self):
        """Return dict of prefix:initial for each :py:attr:`form_classes`."""
        self.forms_initial = self.get_forms_configuration('initial')

    def get_forms(self):
        self.forms = {
            prefix: cls(
                *self.forms_args[prefix],
                **self.forms_kwargs[prefix],
            )
            for prefix, cls in self.form_classes.items()
        }

    def get_forms_args_default(self):
        self.forms_args_default = []
        if self.request.method == 'POST':
            self.forms_args_default = [self.request.POST]

    def get_forms_kwargs_default(self):
        self.form_kwargs_default = dict()
        self.extra_form_kwargs = dict(person=dict())
        person = copy.deepcopy(self.object.insured)
        person.pk = None
        self.extra_form_kwargs['person']['instance'] = person

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
