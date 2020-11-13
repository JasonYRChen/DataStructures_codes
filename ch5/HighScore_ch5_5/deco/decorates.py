import abc


class BaseProperty(abc.ABC):
    def __init__(self):
        self._attr_name = None

    def __get__(self, instance, owner):
        return instance.__dict__[self._attr_name]

    @abc.abstractmethod
    def __set__(self, instance, value):
        pass


class NameProperty(BaseProperty):
    def __set__(self, instance, value):
        if value == '':
            raise ValueError('Name should not be a blank.')
        instance.__dict__[self._attr_name] = value


class PositiveIntegerProperty(BaseProperty):
    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError('Value should be larger than zero.')
        instance.__dict__[self._attr_name] = value


def property_decoration(property=BaseProperty):
    def inner(cls):
        for n, p in cls.__dict__.items():
            if isinstance(p, property):
                p._attr_name = n
        return cls
    return inner
