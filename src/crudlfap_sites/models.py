from django.contrib.sites.models import Site as DjangoSite, SiteManager
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http.request import split_domain_port


class Site(DjangoSite):
    settings = models.JSONField(blank=True, default=dict)
    port = models.PositiveIntegerField(null=True)
    protocol = models.CharField(default='http', max_length=5)

    @property
    def url(self):
        return f'{self.protocol}://{self.domain}'


old_get_current = SiteManager.get_current
DjangoSite.objects.model = Site


def get_current(self, request=None):
    try:
        return old_get_current(self, request)
    except (ImproperlyConfigured, Site.DoesNotExist):
        if not request:
            return Site(domain='localhost', name='localhost')
        host = request.get_host()
        domain, port = split_domain_port(host)
        protocol = request.META['wsgi.url_scheme']
        Site.objects.create(
            name=domain.capitalize(),
            domain=host,
            port=port or 443 if protocol == 'https' else 80,
            protocol=protocol,
        )
    return old_get_current(self, request)


SiteManager.get_current = get_current
