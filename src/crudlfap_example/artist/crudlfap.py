from crudlfap import crudlfap

from .models import Artist


crudlfap.Router(
    Artist,
    fields='__all__',
    paginate_by=3,
    allowed=lambda view: True
).register()
