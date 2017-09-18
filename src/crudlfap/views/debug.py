from django import http
from django.conf import settings
from django.utils.module_loading import import_string
from django.views import generic


class UrlsView(generic.TemplateView):
    template_name = 'crudlfap/debug_urls.html'

    def get(self, request, *a, **k):
        if not request.user.is_superuser:
            return http.HttpResponse404()
        return super(UrlsView, self).get(request, *a, **k)

    def get_context_data(self):
        c = super(UrlsView, self).get_context_data()
        c['urlpatterns'] = urlpatterns = import_string(
            settings.ROOT_URLCONF
        ).urlpatterns
        for u in urlpatterns:
            print(u.regex.pattern, getattr(u, 'url_patterns', None))
        return c
