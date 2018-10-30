"""
This example demonstrates how to use a non-db model for a CRUD.

The model itself, doesn't really make sense here for a real-life app. But it
shows how you can organnize a CRUD around something that's not in the database
nor a managed Django model.

Objects are kept in-memory for this demonstration, but you could use any kind
of remote backend, you will only have to override the methods which are
overridden in this app.

So, basically, you need:

- a model with Meta.managed=False
- override get_queryset() and get_object() in the router,
- override save() and delete() in the model

Oh my, this was too easy, Django I <3 U WILL YOU MARRY ME !! Yes my friend this
is CRUDLFA+ and I can love and marry a software if that's how i feel like
hahahahahahahahahahah oh I'm sorry where you looking for boring software ? lol
"""


from crudlfap import shortcuts as crudlfap

from . import models


class SongRatingRouter(crudlfap.Router):
    def get_queryset(self, view):
        return self.model.objects.object_list

    def get_object(self, view):
        object_list = self.get_queryset(view)
        return object_list[int(view.kwargs['pk']) - 1]


SongRatingRouter(models.SongRating).register()
