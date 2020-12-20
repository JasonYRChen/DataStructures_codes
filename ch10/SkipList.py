from ch10.BaseMap import BaseMap
from collections.abc import Mapping, Sequence


class SkipList(BaseMap):
    class _Node(BaseMap._Item):
        __slots__ = '_key', '_value', '_next', '_prev', '_next_level', '_prev_level'

        def __init__(self, key=[], value=None):
            super().__init__(key, value)
            self._next = None
            self._prev = None
            self._prev_level = None
            self._next_level = None

    def __init__(self, dict_iter=None):
        pass

    def __repr__(self):
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        pass

    def _build_dict(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = list(dict_iter.items())
        elif isinstance(dict_iter, Sequence):
            dict_iter = list(dict_iter)
        else:
            raise TypeError('Invalid type to build a map.')

        # Aware of multiple same keys and make sure uniqueness of the key
        dict_iter = sorted(dict_iter)

    def items(self):
        pass

    def keys(self):
        pass

    def values(self):
        pass


if __name__ == '__main__':
    pass
