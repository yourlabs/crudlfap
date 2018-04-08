class Factory(object):
    @classmethod
    def clone(cls, **attributes):
        """Return a subclass with the given attributes.

        If a model is found, it will prefix the class name with the model.
        """
        name = cls.__name__
        model = attributes.get('model', getattr(cls, 'model', None))
        if model is None:
            model = getattr(cls, 'model', None)
        if model and model.__name__ not in cls.__name__:
            name = '{}{}'.format(model.__name__, cls.__name__)
        return type(name, (cls,), attributes)
