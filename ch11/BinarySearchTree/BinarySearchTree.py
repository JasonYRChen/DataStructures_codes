from ch11.BinarySearchTree.BinaryTree import BinaryTree


class BinarySearchTree(BinaryTree):
    class _Node:
        """ This class may be overridden in the future for map or linked nodes using.
            Ex1. For map, a 'self._value' may needed to save value
            Ex2. For linked nodes, 'self._parent' and 'self._left (_right)' parameters may needed.
        """
        __slots__ = '_key'

        def __init__(self, key=[]):
            self._key = key

        def __lt__(self, other):
            return self._key < other._key

        def __ge__(self, other):
            return self._key >= other._key

        def __le__(self, other):
            return self._key <= other._key

        def __eq__(self, other):
            if other is None:
                return False
            return self._key == other._key

        def __gt__(self, other):
            return self._key > other._key

    def _search_node(self, key, node=None):
        """ Return node on target or the nearest node"""
        node = self._root() if node is None else node
        if not isinstance(node, self._Node):
            return node
        if (key == node._key) or self._is_leaf(node):
            return node
        if (key > node._key) and (self._right(node)):
            return self._search_node(key, self._right(node))
        elif (key < node._key) and (self._left(node)):
            return self._search_node(key, self._left(node))
        return node

    def _before(self, node):
        if self._left(node):
            node = self._left(node)
            while self._right(node):
                node = self._right(node)
            return node
        if node == self._first():
            return None
        parent = self._parent(node)
        while self._left(parent) and node == self._left(parent):
            parent, node = self._parent(parent), parent
        return parent

    def _after(self, node):
        if self._right(node):
            node = self._right(node)
            while self._left(node):
                node = self._left(node)
            return node
        if node == self._last():
            return None
        parent = self._parent(node)
        while self._right(parent) and node == self._right(parent):
            parent, node = self._parent(parent), parent
        return parent

    def _first(self):
        node = self._root()
        while self._left(node):
            node = self._left(node)
        return node

    def _last(self):
        node = self._root()
        while self._right(node):
            node = self._right(node)
        return node

    def _sort(self, start=None, end=None, ascending=True):
        start = self._first() if start is None else start
        end = self._last() if end is None else end
        if start >= end:
            start, end = start, start
        else:
            start, end = (start, end) if ascending else (end, start)
        mode = self._after if ascending else self._before
        func = self._Node.__le__ if ascending else self._Node.__ge__
        while start is not None and func(start, end):
            yield start
            start = mode(start)

    def _is_root(self, node):
        return node == self._root()

    def _children(self, node):
        if self._left(node):
            yield self._left(node)
        if self._right(node):
            yield self._right(node)

    def _children_num(self, node):
        return len(list(self._children(node)))

    def _height(self, node=None):
        node = self._root() if node is None else node
        if self._is_leaf(node):
            return 0
        return 1 + max(self._height(c) for c in self._children(node))

    def _depth(self, node):
        if node == self._root():
            return 0
        return 1 + self._depth(self._parent(node))

    def _is_leaf(self, node):
        return self._children_num(node) == 0
