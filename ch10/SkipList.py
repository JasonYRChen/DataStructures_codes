from ch10.BaseMap import BaseMap
from collections.abc import Mapping, Sequence
from random import randrange
from math import log2, floor


class SkipList(BaseMap):
    class _Node(BaseMap._Item):
        __slots__ = '_key', '_value', '_next', '_prev', '_next_level', '_prev_level'

        def __init__(self, key=['-inf'], value=None):
            super().__init__(key, value)
            self._next = None
            self._prev = None
            self._prev_level = None
            self._next_level = None

        def __repr__(self):
            return f"({self._key}={self._value})"

    def __init__(self, dict_iter=None):
        self._start = None
        self._size = 0
        self._height = 0
        self._initialize_boundary(0)
        if dict_iter:
            self._build_dict(dict_iter)

    def __repr__(self):
        string = [f"{k}={v}" for k, v in self.items()]
        string = ', '.join(string)
        return f"{self.__class__.__name__}({string})"

    def __getitem__(self, key):
        node, _ = self._search_node(key)
        if key == node._key:
            return node._value
        raise KeyError(f'Invalid key {key}')

    def __setitem__(self, key, value):
        node, nodes = self._search_node(key)
        if key == node._key:
            node._value = value
        else:
            self._self_tower(self._Node(key, value), nodes)
            self._size += 1
            if floor(log2(len(self))) > self._height:
                self._build_dict(list(self.items()))

    def __delitem__(self, key):
        node, nodes = self._search_node(key)
        if key != node._key:
            raise KeyError(f'Invalid key {key}')
        prev = nodes.pop()
        while prev._next._key == key:
            prev._next, prev._next._next._prev = prev._next._next, prev
            prev = nodes.pop()
        self._size -= 1

    def __iter__(self):
        yield from self.keys()

    def __len__(self):
        return self._size

    @staticmethod
    def _valid_key(key):
        hash(key)
        return key

    def _search_node(self, key):
        key = self._valid_key(key)
        node = self._start
        nodes = []
        while True:
            while (not node._next._key == ['+inf']) and (key >= node._next._key):
                node = node._next
            nodes.append(node)
            if node._next_level:
                node = node._next_level
            else:
                return node, nodes

    def _self_tower(self, node, nodes):
        build = 1
        next_level = None
        while build and nodes:
            prev = nodes.pop()
            prev._next, node._next = node, prev._next
            node._prev, node._next._prev = prev, node
            node._next_level = next_level
            if next_level:
                next_level._prev_level = node
            node, next_level = self._Node(node._key), node
            build = randrange(2)

    def _initialize_boundary(self, h):
        prevs = (None, None)
        for _ in range(h + 1):
            start, end = self._Node(), self._Node(['+inf'])
            start._next, end._prev = end, start
            start._next_level, end._next_level = prevs
            if prevs[0]:
                prevs[0]._prev_level, prevs[1]._prev_level = start, end
                self._height += 1
            prevs = start, end
        self._start = start

    def _build_dict(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = list(dict_iter.items())
        else:
            dict_iter = list(dict_iter)

        self._size, self._height = 0, 0
        self._initialize_boundary(floor(log2(len(dict_iter))))
        for k, v in dict_iter:
            self[k] = v

    def _main_branch(self):
        node = self._start
        while node._next_level:
            node = node._next_level
        while node._next._key != ['+inf']:
            yield node._next
            node = node._next

    def items(self):
        for node in self._main_branch():
            yield node._key, node._value

    def keys(self):
        for node in self._main_branch():
            yield node._key

    def values(self):
        for node in self._main_branch():
            yield node._value

    def print_all(self):
        pass


if __name__ == '__main__':
    s = SkipList()
    s['c'] = 3
    s['a'] = 1
    s['e'] = 5
    s['f'] = 6
    s['b'] = 2
    print(s)
    print(f"len: {len(s)}, height: {s._height}")