from django import http
from django.conf import settings
from django.utils.module_loading import import_string

from .generic import TemplateView


class UrlsView(TemplateView):
    template_name = 'crudlfap/debug_urls.html'

    def printurl(self, parent, url):
        def url_repr(url):
            pattern = getattr(url, 'pattern', None)
            if pattern:
                regex = getattr(pattern, 'regex', None)
                if regex:
                    return regex.pattern.lstrip(
                        '^').rstrip('$').replace('\/', '/')
            return url_repr or ''
        ret = parent if parent else ''
        ret += url_repr(url)

        self.urlpatterns[ret] = url

        for pattern in getattr(url, 'url_patterns', []):
            self.printurl(ret, pattern)

    def get(self, request, *a, **k):
        urlpatterns = import_string(settings.ROOT_URLCONF).urlpatterns
        self.urlpatterns = {}
        for url in urlpatterns:
            self.printurl('/', url)

        if not request.user.is_superuser:
            return http.HttpResponseNotFound()
        return super(UrlsView, self).get(request, *a, **k)
