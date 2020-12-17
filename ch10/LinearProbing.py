from ch10.BaseHashTable import BaseHashTable
from collections.abc import Mapping, Sequence


class LinearProbing(BaseHashTable):
    def __repr__(self):
        strings = [f"{k}={v}" for k, v in self.items()]
        strings = ', '.join(strings)
        return f"{self.__class__.__name__}({strings})"

    def __getitem__(self, key):
        idx = self._hash_func(key)
        steps = self.collision_step
        for i in range(steps + 1):
            item = self._data[idx + i]
            if key == item._key:
                return item._value
        raise KeyError(f'Invalid key {key}')

    def __setitem__(self, key, value):
        idx = self._hash_func(key)
        steps = min(self.collision_step, len(self._data)-idx-1)
        for i in range(steps + 1):
            item = self._data[idx + i]
            if item._key == key:
                item._value = value
                return
            elif item._key == []:
                self._data[idx + i] = self._Item(key, value)
                self._size += 1
                if (len(self) / self.buckets) > self.load_factor_max:
                    self._resize(2 * self.buckets - 1)
                return
        self._resize(2 * self.buckets - 1)
        self[key] = value

    def __delitem__(self, key):
        idx = self._hash_func(key)
        steps = self.collision_step
        for i in range(steps + 1):
            if key == self._data[idx + i]._key:
                self._data[idx + i] = self._Item()
                self._size -= 1
                if (len(self) / self.buckets) < self.load_factor_min:
                    self._resize((self.buckets + 1) // 2)
                return
        raise KeyError(f"Invalid key {key}")

    def _build_dict(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = list(dict_iter.items())
        elif isinstance(dict_iter, Sequence):
            dict_iter = list(dict_iter)
        else:
            raise TypeError('Invalid type of parameter. Make sure the argument is dict-like or list of tuples')

        for k, v in dict_iter:
            self[k] = v

    def items(self):
        for item in self._data:
            if item._key != []:
                yield item._key, item._value

    def keys(self):
        for item in self._data:
            if item._key != []:
                yield item._key

    def values(self):
        for item in self._data:
            if item._key != []:
                yield item._value


if __name__ == '__main__':
    from string import ascii_letters as al
    a = {c: i for i, c in enumerate(al[:10])}
    b = list(a.items())
    c = {c: i for i, c in enumerate(al[11:19])}
    d = {c: i for i, c in enumerate(al[:15])}
    e = range(10)

    l = LinearProbing(a)
    print('item number:', len(l), 'data length:', len(l._data))
    print(l)
    print(l._data)
    l.update(d)
    print('item number:', len(l), 'data length:', len(l._data))
    print(l)
    print(l._data)
