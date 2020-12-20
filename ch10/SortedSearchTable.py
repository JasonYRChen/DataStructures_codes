from ch10.BaseMap import BaseMap
from collections.abc import Mapping, Sequence


class SortedSearchTable(BaseMap):
    def __init__(self, dict_iter=None):
        self._data = []
        if dict_iter:
            self._build_dict(dict_iter)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        string = [f'{k}={v}' for k, v in self.items()]
        string = ', '.join(string)
        return f"{self.__class__.__name__}({string})"

    def _build_dict(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = list(dict_iter.items())
        elif isinstance(dict_iter, Sequence):
            dict_iter = list(dict_iter)
        else:
            raise TypeError('Make sure the argument is dict-like or list of 2-element tuple')

        for k, v in dict_iter:
            self[k] = v

    def __getitem__(self, key):
        _, item = self._binary_search(key)
        if item is None:
            raise KeyError(f'Invalid key "{key}"')
        return item._value

    def __setitem__(self, key, value):
        idx, item = self._binary_search(key)
        if item is None:
            self._data.insert(idx, self._Item(key, value))
        else:
            item._value = value

    def __delitem__(self, key):
        idx, item = self._binary_search(key)
        if item is None:
            raise KeyError(f'Invalid key "{key}"')
        del self._data[idx]

    def __iter__(self):
        yield from self.keys()

    def __reversed__(self):
        for item in self._data[::-1]:
            yield item._key

    def items(self):
        for item in self._data:
            yield item._key, item._value

    def keys(self):
        for item in self._data:
            yield item._key

    def values(self):
        for item in self._data:
            yield item._value

    def _binary_search(self, key):
        s, e = 0, len(self)
        while s < e:
            mid = (s + e) // 2
            item = self._data[mid]
            if key == item._key:
                return mid, item
            elif key > item._key:
                s = mid + 1
            else:
                e = mid
        return s, None

    def find_min(self):
        return (self._data[0]._key, self._data[0]._value) if len(self) else None

    def find_max(self):
        return (self._data[-1]._key, self._data[-1]._value) if len(self) else None

    def find_lt(self, key):
        idx, _ = self._binary_search(key)
        for item in self._data[:idx]:
            yield item._key, item._value

    def find_le(self, key):
        idx, item = self._binary_search(key)
        if item is None:
            for item in self._data[:idx]:
                yield item._key, item._value
        else:
            for item in self._data[:idx+1]:
                yield item._key, item._value

    def find_gt(self, key):
        idx, item = self._binary_search(key)
        if item is None:
            for item in self._data[idx:]:
                yield item._key, item._value
        else:
            for item in self._data[idx+1:]:
                yield item._key, item._value

    def find_ge(self, key):
        idx, _ = self._binary_search(key)
        for item in self._data[idx:]:
            yield item._key, item._value

    def find_range(self, start, stop):
        for k, v in self.find_ge(start):
            if k >= stop:
                break
            yield k, v


if __name__ == '__main__':
    from string import ascii_letters as al
    a = {c: i for i, c in enumerate(al[:10])}
    b = list(a.items())
    c = {c: i for i, c in enumerate(al[11:19][::-1])}
    d = {c: i for i, c in enumerate(al[:15])}

    s = SortedSearchTable(c)
    del s['o']
    del s['p']
    print(s)
    for k, v in s.find_range('s', 'l'):
        print(k, v)
