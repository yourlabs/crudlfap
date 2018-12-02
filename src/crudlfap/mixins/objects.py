from .model import ModelMixin


class ObjectsMixin(ModelMixin):
    pluralize = True

    def get_objects(self):
        return self.queryset
