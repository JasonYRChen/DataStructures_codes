from collections.abc import MutableMapping
from random import randrange
from accessary.properties import LoadFactorProperty, BucketProperty, PrimeProperty
from accessary.properties import class_property_deco, CollisionStepProperty


@class_property_deco()
class BaseHashTable(MutableMapping):
    load_factor_max = LoadFactorProperty()
    load_factor_min = LoadFactorProperty()
    buckets = BucketProperty()
    prime = PrimeProperty()
    collision_step = CollisionStepProperty()

    class _Item:
        __slots__ = '_key', '_value'

        def __init__(self, key=[], value=None):
            self._key = key
            self._value = value

        def __repr__(self):
            return f"{self._key}={self._value}"

        def __eq__(self, other):
            return (self._key == other._key) and (self._value == other._value)

        def __ne__(self, other):
            return not self == other

    def __init__(self, dict_iter=None):
        with BaseHashTable.__dict__['buckets'] as b, BaseHashTable.__dict__['load_factor_max'] as l_max, \
                BaseHashTable.__dict__['load_factor_min'] as l_min, BaseHashTable.__dict__['prime'] as p, \
                BaseHashTable.__dict__['collision_step'] as c:
            b._pwd = b._PropertyBase__pwd
            p._pwd = p._PropertyBase__pwd
            l_max._pwd = l_max._PropertyBase__pwd
            l_min._pwd = l_min._PropertyBase__pwd
            c._pwd = c._PropertyBase__pwd
            self.load_factor_max = 0.5  # for expanding list
            self.load_factor_min = 0.2  # for shrinking list
            self.buckets = 11
            self.prime = 109345121
            self.collision_step = 1
        self._a = randrange(1, self.prime)
        self._b = randrange(self.prime)
        self._data = [self._Item()] * self.buckets
        self._size = 0
        if dict_iter:
            self._build_dict(dict_iter)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        yield from self.keys()

    def _build_dict(self, dict_iter):
        raise NotImplementedError

    def _hash_func(self, key):
        a, b, p, N = self._a, self._b, self.prime, self.buckets
        return ((a * hash(key) + b) % p) % N

    def _resize(self, buckets):
        old_dict = list(self.items())
        with BaseHashTable.__dict__['buckets'] as b:
            b._pwd = b._PropertyBase__pwd
            self.buckets = buckets
        self._data = [self._Item()] * buckets
        self._size = 0
        self._build_dict(old_dict)

    def items(self):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def values(self):
        raise NotImplementedError


if __name__ == '__main__':
    h = BaseHashTable()
    print(h.buckets)

