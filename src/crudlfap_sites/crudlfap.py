from crudlfap import shortcuts as crudlfap

from .models import Site


crudlfap.Router(model=Site, icon='language').register()
