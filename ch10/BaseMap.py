from collections.abc import MutableMapping


class BaseMap(MutableMapping):
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

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError
