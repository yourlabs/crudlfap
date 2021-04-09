import os

from django import http
from crudlfap.views.generic import View


schema = {
    'basePath': '/v2',
    'definitions': {},
    'info': {},
    'paths': {},
    'schemes': ['https', 'http'],
    'securityDefinitions': {},
    'swagger': '2.0',
    'tags': []
}


class SchemaView(View):
    authenticate = False

    def get(self, request, *args, **kwargs):
        schema['definitions'] = dict()
        schema['paths'] = dict()
        schema['host'] = request.get_host()
        for model, router in self.registry.items():
            for view in router.views:
                view = view.abstract(request=request)
                if not view.has_perm():
                    continue
                if getattr(view, 'router', None):
                    self.add_router_schema(request, view.router, schema)
                try:
                    path_definition = view.swagger_path_definition
                except AttributeError:
                    pass
                else:
                    if path_definition:
                        self.add_path_definition(path_definition, view, schema)
        return http.JsonResponse(schema)

    def add_path_definition(self, path_definition, view, schema):
        url = view.urlpath
        if router := getattr(view, 'router', None):
            if url:
                url = os.path.join(router.urlpath, url)
            else:
                url = router.urlpath
        if self.registry.urlpath:
            url = self.registry.urlpath + url
        url = '/' + url.replace('<', '{').replace('>', '}')
        schema['paths'][url] = path_definition

    def add_router_schema(self, request, router, schema):
        try:
            model_name = router.get_swagger_model_name(request)
        except AttributeError:
            pass
        else:
            if model_name and model_name not in schema['definitions']:
                model_definition = router.get_swagger_model_definition(request)
                if model_definition:
                    schema['definitions'][model_name] = model_definition
