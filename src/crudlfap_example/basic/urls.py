from crudlfap import crudlfap

from .models import Artist


urlpatterns = crudlfap.Router(Artist).urlpatterns()
