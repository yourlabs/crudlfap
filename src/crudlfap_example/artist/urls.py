from crudlfap import crudlfap

from .models import Artist


urlpatterns = crudlfap.Router(Artist, fields='__all__', fa_icon='music').urlpatterns()
