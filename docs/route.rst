View URL autogeneration mechanisms: RoutableViewMixin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the key architectural concepts of CRUDLFA+ is the ability for views to
generate their own URLs. This chapter reviews the different mechanisms in place
and how they are overridable.

Code which makes a view encapsulate what it takes to make it auto generate urls
is located in the :py:class:`~crudlfap.route.Route`, which
we'll describe intensively here.

.. automodule:: crudlfap.route
   :members:
