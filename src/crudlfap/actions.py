"""
The Action class in CRUDLFA+'s pattern to generate views on the fly.

How did we land here ? An obsessionnal refactoring spree on the CRUD design
pattern. And despite how technicaly obscene is this python implementation,
we hope you have a lot of fun implementing your own actions, ie:

.. code-block:: py

    # Absolute minimum
    class FormatAction(crudlfap.Action):
        def form_valid(self, form):
            self.object.format(with_ie=WHYYYYYY)

Example overriding default view parents in :py:meth:`Action.generate_views`:

.. code-block:: py

    class FormatAction(crudlfap.Action):
        form_class = YourForm

        class ObjectView:
            success_message = 'formated 1 object!'

        class ObjectsView:
            success_message = 'formated at least one object!'

        # write shared code in Action:
        def form_valid(self, form):
            if 'pks' in self.request.GET:
                # lol yes its as simple as that
            self.object.format(with_ie=WHYYYYYY)
"""
from crudlfap.factory import Factory
from crudlfap.views.generic import ObjectFormView
from crudlfap.views.list import ObjectsFormView

from django import forms
from django.contrib import messages
from django.contrib.admin.models import DELETION
from django.utils.translation import ugettext as _


class Action(Factory):
    """
    Generate views to work on single and multiple objects.

    This defaults to being a modal controller with an empty Django form_class.
    For gory details see :py:meth:`generate_views`.
    """

    controller = 'modal'
    action = 'click->modal#open'
    form_class = forms.Form

    class ObjectView:
        """
        First parent for the view that should be compatible with
        :py:class:`~crudlfap.views.generic.ObjectFormView`, to work with single
        objects.

        You are welcome to override this class.

        .. py:attribute:: menus

            Defaults to the object and object_detail menus.
        """
        menus = ['object', 'object_detail']

    class ObjectsView:
        """
        First parent for the view that should be compatible with
        :py:class:`~crudlfap.views.generic.ObjectsFormView`, to work with
        multiple objects.

        You are welcome to override this class.

        .. py:attribute:: menus

            Add to list_action menu.

        .. py:attribute:: link_attributes

            Connect the list action controller.
        """
        link_attributes = {
            'data-listaction': 'urlupdate',
        }
        menus = ['list_action']

    def generate_views(self):
        """Cook a couple of views that can share code."""
        return [
            type(
                self.cls.__name__.replace('Action', 'View'),
                (self.ObjectView, self.cls, ObjectFormView),
                dict()
            ),
            type(
                self.cls.__name__.replace('Action', 'SelectedView'),
                (self.ObjectsView, self.cls, ObjectsFormView),
                dict()
            )
        ]


class DeleteAction(Action):
    """View to delete a model object."""

    default_template_name = 'crudlfap/delete.html'
    style = 'danger'
    fa_icon = 'trash'
    material_icon = 'delete'
    success_url_next = True
    color = 'red'
    log_action_flag = DELETION
