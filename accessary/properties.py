class PropertyBase:
    __pwd = 'abc'

    def __init__(self, *, password=None):
        self._param = None
        self._pwd = password

    def __get__(self, instance, owner):
        return instance.__dict__[self._param]

    def __set__(self, instance, value):
        if self._pwd is None:
            pwd = input('Enter password: ')
        if self._pwd == self.__pwd or pwd == self.__pwd:
            instance.__dict__[self._param] = value
            self._pwd = None
        else:
            print(f'Invalid password. Set {self._param} failed.')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pwd = None


class LoadFactorProperty(PropertyBase):
    def __set__(self, instance, value):
        if not 0 < value <= 1:
            raise ValueError('Invalid load factor value. Make sure 0 < load factor <= 1.')
        super().__set__(instance, value)


class BucketProperty(PropertyBase):
    def __set__(self, instance, value):
        if value <= 0 or not isinstance(value, int):
            raise ValueError('Invalid bucket number setting. Make sure it is an integer and larger than zero.')
        try:
            prime = instance.prime
        except KeyError:
            pass
        else:
            if prime <= value:
                raise ValueError(f'Bucket number should smaller than prime. Current prime: {instance.prime}')
        super().__set__(instance, value)


class PrimeProperty(PropertyBase):
    def __set__(self, instance, value):
        if value <= 1 or not isinstance(value, int):
            raise ValueError('Invalid prime number. Make sure it is an integer and larger than one.')
        try:
            buckets = instance.buckets
        except KeyError:
            pass
        else:
            if buckets >= value:
                raise ValueError(f'Prime number should larger than bucket number. Current bucket number: {instance.buckets}')
        super().__set__(instance, value)


class CollisionStepProperty(PropertyBase):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Collision step should be non-negative integer')
        super().__set__(instance, value)


def class_property_deco(prop=PropertyBase):
    def inner(cls):
        for name, descriptor in cls.__dict__.items():
            if isinstance(descriptor, prop):
                descriptor._param = name
        return cls
    return inner
