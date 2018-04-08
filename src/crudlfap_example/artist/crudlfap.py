from crudlfap import crudlfap

from .models import Artist


crudlfap.Router(
    Artist,
    fields='__all__',
    allowed=True
).register()
