from ch11.TreeMapLinkedList import TreeMapLinkedList
from math import log2, ceil


class AVLTree(TreeMapLinkedList):
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
            self._rebalance(new_node)
        else:
            node._value = value

    def __delitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if key != node._key:
            raise KeyError(f"Invalid key {key}")
        self._size -= 1
        node = self._delete(node)
        # children_num = self._children_num(node)
        # if children_num == 1:


    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node._left), self._height(node._right))

    def _rebalance(self, node, method=None):
        if method is None:
            method = self._rotation_rebalance
        method(node)

    def _rotation_rebalance(self, node):
        while node._parent is not None and node._parent._parent is not None:
            l_height = self._height(node._parent._parent._left)
            r_height = self._height(node._parent._parent._right)
            if abs(l_height - r_height) > 1:
                return self._rotate(node)
            node = node._parent

    def _rotate(self, node):
        parent, grand_parent = node._parent, node._parent._parent
        if (parent <= node <= grand_parent) or (parent > node > grand_parent):
            self._interchange(node, parent)
            parent = node
        return self._interchange(parent, grand_parent)

    def _interchange(self, node, parent):
        node._parent = parent._parent
        if parent._parent is None:
            self._root_node = node
        elif parent._parent._left and parent._parent._left == parent:
            parent._parent._left = node
        elif parent._parent._right and parent._parent._right == parent:
            parent._parent._right = node

        if parent._left and node == parent._left:
            node._right, parent._left = parent, node._right
            if parent._left:
                parent._left._parent = parent
        else:
            node._left, parent._right = parent, node._left
            if parent._right:
                parent._right._parent = parent
        parent._parent = node
        return node




    def __getitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if key != node._key:
            raise KeyError(f"Invalid key {key}")
        return node


if __name__ == '__main__':
    from string import ascii_letters as al

    a = {(k, v) for v, k in enumerate(al[:20], 1)}
    b = [(k, v) for v, k in enumerate(al[:10][::-1], 1)]
    c = [('c', 3), ('a', 1), ('d', 4), ('i', 9), ('g', 7), ('e', 5), ('b', 2), ('f', 6), ('j', 10), ('h', 8)]
    d = [('c', 3), ('b', 2), ('a', 1)]
    t = AVLTree(a)
    print('len:', len(t))
    print(t)
    t._print_all()
