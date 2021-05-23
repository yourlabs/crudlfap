CRUDLFA+ Tutorial
~~~~~~~~~~~~~~~~~

About document
==============

This document attempts to teach the patterns you can use, and at the same time
go through every feature. The document strives to teach CRUDLFA+ as efficiently
as possible. If it becomes too long, we will see how we refactor the document,
until then, it serves as main documentation. Please contribute any modification
you feel this document needs to fit its purpose.

About module
============

CRUDLFA+ strives to provide a modern UI for Django generic views out of the
box, but all defaults should also be overiddable as conveniently as possible.
It turns out that Django performs extremely well already, and pushing Django's
philosophy such as DRY as far as possible works very well for me.

Start a CRUDLFA+ project
========================

Make sure you install all project dependencies::

    pip install crudlfap[project]

And create a Django project::

    django-admin startproject yourproject

Copy this ``settings.py`` which provides working settings for CRUDLFA+
and allows to control settings with environment variables:

.. literalinclude:: ../src/crudlfap_example/settings.py

And this ``urls.py``:

.. literalinclude:: ../src/crudlfap_example/urls.py

You may also install manually, but the procedure might change over time.

Create a ``crudlfap.py``
========================

You need to create a Django app like with ``./manage.py startapp yourapp``. It
creates a yourapp directory and you need to add yourapp to
``settings.INSTALLED_APPS``.

Then, you can start a ``yourapp/crudlfap.py`` file, where you can define model
CRUDs, hook into the rendering of CRUDLFA+ (ie. menus) and so on.

Define a Router
===============

Register a CRUD with default views using Router.register()
----------------------------------------------------------

Just add a ``crudlfap.py`` file in one of your installed apps, and the
:py:class:`~crudlfap.apps.DefaultConfig` will autodiscover them, this example
shows how to enable the default CRUD for a custom model:

.. literalinclude:: ../src/crudlfap_example/artist/crudlfap.py

In this case, the :py:class:`~crudlfap.router.Router` will get the views
it should serve from the :py:data:`~crudlfap.settings.CRUDLFAP_VIEWS`
setting.

Custom view parameters with View.clone()
----------------------------------------

If you want to specify views in the router:

.. literalinclude:: ../src/crudlfap_example/song/crudlfap.py

Using the :py:meth:`~crudlfap.factory.Factory.clone()` classmethod will
define a subclass on the fly with the given attributes.

URLs
====

The easiest configuration is to generate patterns from the default registry::

    from crudlfap import shortcuts as crudlfap

    urlpatterns = [
        crudlfap.site.urlpattern
    ]

Or, to sit in ``/admin``::

    crudlfap.site.urlpath = 'admin'

    urlpatterns = [
        crudlfap.site.urlpattern,
        # your patterns ..
    ]

Changing home page
==================

CRUDLFA+ so far relies on Jinja2 and provides a configuration
where it finds templates in app_dir/jinja2.

As such, a way to override the home page template is to create a directory
"jinja2" in one of your apps - personnaly i add the project itself to
INSTALLED_APPS, sorry if you have hard feelings about it but i love to do
that, have a place to put project-specific stuff in general - and in the
`jinja2` directory create a `crudlfap/home.html` file.

You will also probably want to override `crudlfap/base.html`. But where it
gets more interresting is when you replace the home view with your own.
Example, still in urls.py::

    from crudlfap import shortcuts as crudlfap
    from .views import Dashboard  # your view

    crudlfap.site.title = 'Your Title'  # used by base.html
    crudlfap.site.urlpath = 'admin'  # example url prefix
    crudlfap.site.views['home'] = views.Dashboard

    urlpatterns = [
        crudlfap.site.get_urlpattern(),
    ]

So, there'd be other ways to acheive this but that's how i like to
do it.

Add menu item
=============

You can hook into CRUDLFA+ menu rendering, ie.:

.. literalinclude:: ../src/crudlfap_registration/crudlfap.py

Create route from view
======================

The following example returns a :py:class:`~crudlfap.route.Route` as needed by
:py:class:`~crudlfap.router.Router` and
:py:class:`~crudlfap.registry.Registry`:

.. code-block:: python

    Route.factory(
        LoginView,
        title=_('Login'),
        title_submit=_('Login'),
        title_menu=_('Login'),
        menus=['main'],
        redirect_authenticated_user=True,
        authenticate=False,
        icon='login',
        has_perm=lambda self: not self.request.user.is_authenticated,
    )

Useful to add external apps views to routers or site.views, prior to the menu
hook feature.

Create list actions
===================

List actions, such as the delete action, can be implemented as such::

    class DeployMixin(crudlfap.ActionMixin):
        style = ''
        icon = 'send'
        success_url_next = True
        color = 'green'
        form_class = forms.Form
        permission_shortcode = 'send'
        label = 'deploy'

        def get_success_url(self):
            return self.router['list'].reverse()

        def has_perm_object(self):
            return self.object.state == 'held'


    class TransactionDeployView(DeployMixin, crudlfap.ObjectFormView):
        def form_valid(self):
            self.object.state = 'deploy'
            self.object.save()
            return super().form_valid()


    class TransactionDeployMultipleView(DeployMixin, crudlfap.ObjectsFormView):
        def form_valid(self):
            self.object_list.filter(state='held').update(state='deploy')
            return super().form_valid()

API
===

CRUDLFA+ now offers a REST API interface which is documented with swagger on
``/api``.

Usage
-----

It requires to set the ``Content-Type: application/json`` header. For example:

.. code-block:: python

    import requests

    response = requests.get(
        f'http://localhost:8000/blockchain',
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    blockchains = response.json()

POST requests require a CSRF token that you may obtain as a cookie with any GET
request, but it is advised that you keep it up to date by using a request
session.

.. code-block:: python

    import requests
    session = requests.session()
    session.get('http://localhost:8000')
    response = session.post(
        f'{site}/auth/login/',
        dict(
            username='user', password='user'
        ),
        headers={'X-CSRFToken': session.cookies['csrftoken']},
        allow_redirects=False,
    )
    assert response.status_code == 302


Then you can make more POST requests ie. to create an object:

.. code-block:: python

    response = session.post(
        f'{site}/account/create',
        json=dict(
            blockchain=123,
        ),
        headers={
            'Content-Type': 'application/json',
            'X-CSRFToken': session.cookies['csrftoken'],
        }
    )
    assert response.status_code == 201

In case of error, it will return a 4xx response with the error details in a
JSON response.

Customize the API
-----------------

By default, views will call the router's
:py:meth:`~crudlfap.router.Router.serialize(obj, fields)` method. You may override it,
or just configure :py:attr:`~crudlfap.router.Router.json_fields` attribute. To
serialize each field, it will try to find ``get_FIELDNAME_json()`` method,
otherwise use the default
:py:meth:`~crudlfap.router.Router.get_FIELDNAME_json(obj, field)` method which
you might has well override. It will use the related router to serialize any
related object.

Then, you may override both of these at the view level if you want.
