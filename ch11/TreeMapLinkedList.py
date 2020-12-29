from ch11.BinarySearchTree.BinarySearchTree import BinarySearchTree
from collections.abc import MutableMapping, Mapping
from math import floor, log2


class TreeMapLinkedList(BinarySearchTree, MutableMapping):
    class _Node(BinarySearchTree._Node):
        __slots__ = '_key', '_value', '_parent', '_left', '_right'

        def __init__(self, key=None, value=None, parent=None, left=None, right=None):
            super().__init__(key)
            self._value = value
            self._parent = parent
            self._left = left
            self._right = right

        def __repr__(self):
            return f"({self._key}={self._value}, p={self._parent._key if self._parent else None}, l={self._left._key if self._left else None}, r={self._right._key if self._right else None})"

    def __init__(self, dict_iter=None):
        self._size = 0
        self._root_node = None
        if dict_iter:
            self._build_map(dict_iter)

    def __repr__(self):
        if self._root():
            string = [f"{n._key}={n._value}" for n in self._sort()]
            string = ', '.join(string)
        else:
            string = ''
        return f"{self.__class__.__name__}({string})"

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if key != node._key:
            raise KeyError(f"Invalid key {key}")
        return node._value

    def __setitem__(self, key, value):
        key = self._valid_key(key)
        node = self._search_node(key)
        if node is None or key != node._key:
            new_node = self._Node(key, value, node)
            if node is None:
                self._root_node = new_node
            elif key < node._key:
                node._left = new_node
            else:
                node._right = new_node
            self._size += 1
        else:
            node._value = value

    def __delitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if key != node._key:
            raise KeyError(f"Invalid key {key}")
        self._delete(node)
        self._size -= 1

    def __iter__(self):
        for node in self._sort():
            yield node._key

    def _delete(self, node):
        children = list(self._children(node))
        children_num = len(children)
        if children_num < 2:
            if self._is_root(node):
                self._root_node = None if children == [] else children[0]
            elif node._parent._left and node == node._parent._left:
                node._parent._left = None if children == [] else children[0]
            elif node._parent._right:
                node._parent._right = None if children == [] else children[0]
            if children:
                children[0]._parent = node._parent
            self._node_initialize(node)
        else:
            node_before = self._before(node)
            new_key, new_value = node_before._key, node_before._value
            self._delete(node_before)
            node._key, node._value = new_key, new_value

    def _build_map(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = dict_iter.items()
        for k, v in dict_iter:
            self[k] = v

    def _node_initialize(self, node):
        node._key, node._value, node._parent, node._left, node._right = None, None, None, None, None

    def _valid_key(self, key):
        hash(key)
        return key

    def _root(self):
        return self._root_node

    def _parent(self, node):
        return node._parent

    def _left(self, node):
        return node._left

    def _right(self, node):
        return node._right

    def _print_all(self, node=None, level=0):
        node = self._root() if node is None else node
        if node is None:
            return
        if node._left:
            self._print_all(node._left, level+1)
        print('    ' * level, node, sep='')
        if node._right:
            self._print_all(node._right, level+1)


if __name__ == '__main__':
    from string import ascii_letters as al

    a = {(k, v) for v, k in enumerate(al[:10], 1)}
    b = [(k, v) for v, k in enumerate(al[:10][::-1], 1)]
    t = TreeMapLinkedList(a)
    # t['m'] = 13
    # t['f'] = 6
    # t['a'] = 1
    # t['d'] = 4
    # t['c'] = 3
    # t['e'] = 5
    # t['a'] = 11
    # t['s'] = 19
    # t['n'] = 14
    # t['z'] = 26
    # t['w'] = 23
    # t['i'] = 9
    # t['g'] = 7
    # t['h'] = 8
    print('len:', len(t))
    print(t)
    t._print_all()
    print('len:', len(t), 'floor:', floor(log2(len(t))), 'height:', t._height())
    # del t['f']
    # # del t['w']
    # print('len:', len(t))
    # print(t)
    # t._print_all()

