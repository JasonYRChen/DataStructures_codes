from ch11.TreeMapLinkedList import TreeMapLinkedList


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
        else:
            node._value = value

    def __delitem__(self, key):
        key = self._valid_key(key)
        node = self._search_node(key)
        if key != node._key:
            raise KeyError(f"Invalid key {key}")
        node = self._delete(node)
        self._size -= 1
        self._node_initialize(node)

    def _rebalance(self, node):
        pass

    def _rotate(self, node):
        pass

    def _interchange(self, node, parent):
        pass


if __name__ == '__main__':
    from string import ascii_letters as al
    from random import shuffle

    a = AVLTree()
