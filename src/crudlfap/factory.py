import inspect


class FactoryMetaclass(type):
    def __getattr__(cls, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}'.format(attr[4:], attr))

        getter = getattr(cls, 'get_' + attr)

        if inspect.ismethod(getter):
            return getter()
        else:
            return getter(cls)

    def get_cls(cls):
        return cls


class Factory(metaclass=FactoryMetaclass):
    def __getattr__(self, attr):
        if attr.startswith('get_'):
            raise AttributeError('{} or {}()'.format(attr[4:], attr))

        getter = getattr(self, 'get_{}'.format(attr), None)

        if getter:
            methresult = getter()
            dictresult = self.__dict__.get(attr, None)
            if methresult is None and dictresult is not None:
                result = dictresult
            else:
                result = methresult
            return result

        # Try class methods
        return getattr(type(self), attr)

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
