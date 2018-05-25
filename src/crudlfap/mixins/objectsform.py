from .modelform import ModelFormMixin


class ObjectsFormMixin(ModelFormMixin):
    pluralize = True

    def get_queryset(self):
        return super().get_queryset().filter(
            pk__in=self.request.GET.getlist('pks')
        )

    def form_valid(self, form):
        for obj in self.object_list:
            self.object = obj
            response = super().form_valid(form)
        return response

    def get_success_url(self):
        return self.router['list'].reverse()

