from ch11.BinarySearchTree.BinarySearchTree import BinarySearchTree
from collections.abc import MutableMapping, Mapping
from collections import deque


class TreeMapList(BinarySearchTree, MutableMapping):
    class _Node(BinarySearchTree._Node):
        __slots__ = '_key', '_value', '_index', '_index_to_be'

        def __init__(self, key=[], value=None, index=None, index_to_be=None):
            super().__init__(key)
            self._value = value
            self._index = index
            self._index_to_be = index_to_be

        def __repr__(self):
            return f"({self._key}={self._value}, i={self._index})"

    def __init__(self, dict_iter=None):
        self._data = [None]
        self._size = 0
        if dict_iter:
            self._build_map(dict_iter)

    def __len__(self):
        return self._size

    def __repr__(self):
        string = []
        node = self._first()
        while node:
            string.append(f"{node._key}={node._value}")
            node = self._after(node)
        string = ', '.join(string)
        return f"{self.__class__.__name__}({string})"

    def __setitem__(self, key, value):
        if len(self) == 0:
            self._add_root(key, value)
        else:
            key = self._valid_key(key)
            node = self._search_node(key)
            if node._key == key:
                node._value = value
            else:
                idx = (2 * node._index + 2) if key > node._key else (2 * node._index + 1)
                if idx >= len(self._data):
                    self._extend_space(len(self._data) + 1)
                self._data[idx] = self._Node(key, value, idx)
                self._size += 1

    def __getitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if node._key != key:
            raise KeyError(f"Invalid key {key}")
        return node._value

    def __delitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if node._key != key:
            raise KeyError(f"Invalid key {key}")
        self._delete(node)
        self._size -= 1

    def __iter__(self):
        node = self._first()
        while node:
            yield node._key
            node = self._after(node)

    def _delete(self, node):
        children = list(self._children(node))
        if len(children) == 0:
            self._data[node._index] = None
        elif len(children) == 1:
            child = children[0]
            child._index_to_be = node._index
            temp = [child]
            nodes = deque([child])
            while temp:
                node = temp.pop()
                for c in self._children(node):
                    grand_parent = self._parent(self._parent(c))
                    c._index_to_be = 2*grand_parent._index+1 if c._index % 2 else 2*grand_parent._index+2
                    temp.append(c)
                    nodes.append(c)
            while nodes:
                node = nodes.popleft()
                self._data[node._index_to_be], self._data[node._index] = self._data[node._index], None
                node._index, node._index_to_be = node._index_to_be, None
        else:
            self._data[node._index] = self._before(node)
            self._delete(self._before(node))
            self._data[node._index]._index = node._index

    def _parent(self, node):
        if node._index == 0:
            return None
        return self._data[(node._index - 1) // 2]

    def _left(self, node):
        node_idx = node._index
        left_idx = 2 * node_idx + 1
        if left_idx >= len(self._data):
            return None
        return self._data[left_idx]

    def _right(self, node):
        node_idx = node._index
        right_idx = 2 * node_idx + 2
        if right_idx >= len(self._data):
            return None
        return self._data[right_idx]

    def _root(self):
        return self._data[0]

    def _add_root(self, key, value):
        self._data[0] = self._Node(key, value, 0)
        self._size += 1

    def _build_map(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = dict_iter.items()
        dict_iter = list(dict_iter)
        self._size = 0
        self._data = [None] * len(dict_iter)
        self._add_root(dict_iter[0][0], dict_iter[0][1])
        for k, v in dict_iter[1:]:
            self[k] = v

    def _extend_space(self, amount):
        self._data.extend([None] * amount)

    def _valid_key(self, key):
        hash(key)
        return key

    def _print_all(self, node=None, level=0):
        node = self._root() if node is None else node
        if node is None:
            return
        if self._left(node):
            self._print_all(self._left(node), level+1)
        print('    ' * level, node, sep='')
        if self._right(node):
            self._print_all(self._right(node), level+1)


if __name__ == '__main__':
    from string import ascii_letters as al

    a = [(c, v) for v, c in enumerate(al[:10], 1)]
    b = [(c, v) for v, c in enumerate(al[:10][::-1], 1)]
    t = TreeMapList()
    t['e'] = 5
    t['a'] = 1
    t['l'] = 12
    t['z'] = 26
    t['b'] = 2
    t['d'] = 4
    t['c'] = 3
    t['f'] = 6
    print('len:', len(t), 'array size:', len(t._data))
    print(t)
    print(t._data)
    t._print_all()
    # del t['e']
    # print('len:', len(t), 'array size:', len(t._data))
    # print(t)
    # print(t._data)
    # t._print_all()
    for node in t._sort(t._data[2], t._data[1], ascending=False):
        print(node._key, node._value)
