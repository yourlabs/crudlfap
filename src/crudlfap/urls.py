from django.conf.urls import url

from .views.debug import UrlsView


urlpatterns = [
    url(r'$', UrlsView.as_view(), name='crudlfap'),
]
