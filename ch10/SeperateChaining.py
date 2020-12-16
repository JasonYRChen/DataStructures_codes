from ch10.BaseHashTable import BaseHashTable
from collections.abc import Mapping, Sequence


class SeperateChaining(BaseHashTable):
    def __repr__(self):
        strings = []
        for k, v in self:
            strings.append(f"{k}={v}")
        strings = ', '.join(strings)
        return f"{self.__class__.__name__}({strings})"

    def __getitem__(self, key):
        idx = self._hash_func(key)
        bucket = self._data[idx]
        if isinstance(bucket, list):
            for item in bucket:
                if item._key == key:
                    return item._value
        raise KeyError(f'Invalid key {key}')

    def __setitem__(self, key, value):
        idx = self._hash_func(key)
        bucket = self._data[idx]
        if isinstance(bucket, list):
            for item in bucket:
                if item._key == key:
                    item._value = value
                    return
            else:
                bucket.append(self._Item(key, value))
        if isinstance(bucket, self._Item):
            self._data[idx] = [self._Item(key, value)]
        self._size += 1
        if len(self) / self.buckets >= self.load_factor_max:
            self._resize(2 * self.buckets)

    def __delitem__(self, key):
        idx = self._hash_func(key)
        bucket = self._data[idx]
        if isinstance(bucket, list):
            for i in range(len(bucket)):
                if bucket[i]._key == key:
                    del bucket[i]
                    self._size -= 1
                    if not bucket:
                        self._data[idx] = self._Item()
                    if len(self) / self.buckets < self.load_factor_min:
                        self._resize(self.buckets // 2)
                    return
        raise KeyError(f'Invalid key {key}')

    def _build_dict(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = list(dict_iter.items())
        elif isinstance(dict_iter, list):
            dict_iter = list(dict_iter)
        else:
            raise TypeError('Invalid type of instance. Make sure the argument is dict-like or list of tuples')

        self._size = 0
        for key, value in dict_iter:
            self[key] = value

    def items(self):
        for bucket in self._data:
            if not isinstance(bucket, self._Item):
                for item in bucket:
                    yield item._key, item._value

    def keys(self):
        for bucket in self._data:
            if not isinstance(bucket, self._Item):
                for item in bucket:
                    yield item._key

    def values(self):
        for bucket in self._data:
            if not isinstance(bucket, self._Item):
                for item in bucket:
                    yield item._value


if __name__ == '__main__':
    from string import ascii_letters as al
    a = {c: i for i, c in enumerate(al[:10])}
    b = list(a.items())
    c = {c: i for i, c in enumerate(al[:1])}
    d = {c: i for i, c in enumerate(al[:15])}
    h = SeperateChaining(a)
    print('item number:', len(h), 'data length:', len(h._data))
    print(h)
    h2 = SeperateChaining(c)
    print('item number:', len(h2), 'data length:', len(h2._data))
    print('item number:', len(h), 'data length:', len(h._data))
    print(h2)
    h3 = SeperateChaining(d)
    print('item number:', len(h3), 'data length:', len(h3._data))
    print('item number:', len(h2), 'data length:', len(h2._data))
    print('item number:', len(h), 'data length:', len(h._data))
    print(h3)
