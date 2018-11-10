from crudlfap import shortcuts as crudlfap

from .models import Artist


crudlfap.Router(
    Artist,
    fields='__all__',
).register()
