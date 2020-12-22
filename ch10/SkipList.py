from ch10.BaseMap import BaseMap
from collections.abc import Mapping
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
            if self._key == ['-inf'] or self._key == ['+inf']:
                return f"({self._key})"
            return f"({self._key}={self._value})"
            # return f"(k={self._key}, n={self._next._key if self._next is not None else None}, p={self._prev._key if self._prev is not None else None}, pl={self._prev_level._key if self._prev_level is not None else None}, nl={self._next_level._key if self._next_level is not None else None}) "

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
                self._build_dict(self.items())

    def __delitem__(self, key):
        node, nodes = self._search_node(key)
        if key != node._key:
            raise KeyError(f'Invalid key {key}')

        while nodes:
            pop_node = nodes.pop()
            if pop_node._key == key:
                pop_node._prev._next, pop_node._next._prev = pop_node._next, pop_node._prev
            else:
                break
        self._size -= 1
        if floor(log2(len(self))) < self._height:
            self._build_dict(self.items())

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

    def print_all(self, node=None, seq={}, column_width=10):
        if node is None:
            node = self._start
        if node._next_level:
            self.print_all(node._next_level, seq)
            nodes_before = 0
            while node:
                space = (seq[str(node._key)] - nodes_before - 1) * column_width
                print(f"{' ' * space}{str(node):{column_width}}", end='')
                nodes_before = seq[str(node._key)]
                node = node._next
            print()
        else:
            n = 0
            while node:
                print(f"{str(node):{column_width}}", end='')
                seq[str(node._key)] = n
                node = node._next
                n += 1
            print()


if __name__ == '__main__':
    from string import ascii_letters as al

    a = {k: v for v, k in enumerate(al[:4])}
    b = list(a.items())
    c = {k: v for v, k in enumerate(al[6:10])}
    s = SkipList(b)
    # s['c'] = 3
    # s['a'] = 11
    # s['e'] = 5
    # s[['a']] = 6
    # s['z'] = 2
    print(s)
    print(f"len: {len(s)}, height: {s._height}")
    s.print_all()
    # del s['h']
    # print(s)
    # print(f"len: {len(s)}, height: {s._height}")
    # s.print_all()
    s.update(c)
    print(s)
    print(f"len: {len(s)}, height: {s._height}")
    s.print_all()
