from crudlfap import crudlfap

from .models import Artist


crudlfap.Router(
    Artist,
    fields='__all__',
    # Optionnal hack to allow unauthenticated access:
    allowed=lambda view: True
).register()
