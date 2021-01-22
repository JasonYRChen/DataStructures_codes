from collections.abc import Mapping


class TwoChildrenError(Exception):
    pass


class BinarySearchTree:
    class _Node:
        __slots__ = 'key', 'value', 'left', 'right', 'parent'

        def __init__(self, key=None, value=None, parent=None, left=None, right=None):
            self.key = key
            self.value = value
            self.parent = parent
            self.left = left
            self.right = right

        def __repr__(self):
            return f"k={self.key}, v={self.value}," \
                   f"p={self.parent.key if self.parent else None}, " \
                   f"l={self.left.key if self.left else None}," \
                   f"r={self.right.key if self.right else None}"

    def __init__(self, dict_iter=None):
        self._root = None
        self._size = 0
        if dict_iter:
            self._build_map(dict_iter)

    def __repr__(self):
        first_node = self._first()
        nodes = [node for node in self._inorder_traversal(first_node)] if first_node else []
        return f"{self.__class__.__name__}({', '.join(str(node.key)+'='+str(node.value) for node in nodes)})"

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        key = self.valid_key(key)
        node = self.search(key, self._root)
        if node is None or key != node.key:
            new_node = self._Node(key, value, node)
            if node is None:
                self._root = new_node
            elif key > node.key:
                node.right = new_node
            else:
                node.left = new_node
            self._size += 1
        else:
            node.value = value

    def __getitem__(self, key):
        key = self.valid_key(key)
        node = self.search(key, self._root)
        if key != node.key:
            raise KeyError(f"Invalid key '{key}'")
        return node.value

    def __delitem__(self, key):
        key = self.valid_key(key)
        node = self.search(key, self._root)
        if key != node.key:
            raise KeyError(f"Invalid key '{key}'")
        if node.left and node.right:
            raise TwoChildrenError(f'Two children attach to current node. Deletion failed.')

        child = node.left if node.left else node.right
        if self.is_root(node):
            self._root = child
        else:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
        if child:
            child.parent = node.parent
        self._size -= 1
        return node.value

    def search(self, key, node):
        if node is None:
            return None  # should only be reached when self._root is None
        if key > node.key and node.right:
            return self.search(key, node.right)
        if key < node.key and node.left:
            return self.search(key, node.left)
        return node

    def _first(self):
        node = self._root
        if node is None:
            return None
        while node.left:
            node = node.left
        return node

    @staticmethod
    def before(node):
        if node.left:
            node = node.left
            while node.right:
                node = node.right
            return node

        parent = node.parent
        while parent is not None:
            if node == parent.right:
                return parent
            node, parent = parent, parent.parent
        return None

    @staticmethod
    def after(node):
        if node.right:
            node = node.right
            while node.left:
                node = node.left
            return node

        parent = node.parent
        while parent is not None:
            if node == parent.left:
                return parent
            node, parent = parent, parent.parent
        return None

    def _inorder_traversal(self, start_node):
        yield start_node
        next_node = self.after(start_node)
        while next_node:
            yield next_node
            next_node = self.after(next_node)

    def _preorder(self, node, level):
        yield node, level
        if node.left:
            yield from self._preorder(node.left, level+1)
        if node.right:
            yield from self._preorder(node.right, level+1)

    @staticmethod
    def valid_key(key):
        hash(key)
        return key

    def _build_map(self, dict_iter):
        if isinstance(dict_iter, Mapping):
            dict_iter = dict_iter.items()
        for k, v in dict_iter:
            self[k] = v

    def is_root(self, node):
        return node == self._root

    @staticmethod
    def is_leaf(node):
        return (node.left is None) and (node.right is None)

    def print_all(self, rate=4):
        for node, level in self._preorder(self._root, 0):
            print(' ' * level * rate, node, sep='')


if __name__ == '__main__':
    a = [(7, 'h'), (13, 'n'), (14, 'o'), (6, 'g'), (4, 'e'), (12, 'm'), (8, 'i'), (2, 'c'), (5, 'f'), (0, 'a'), (3, 'd'), (10, 'k'), (1, 'b'), (9, 'j'), (11, 'l')]
    b = dict(a)
    bst = BinarySearchTree()
    for k, v in a[:]:
        bst[k] = v
    print(bst)
    print(len(bst))
    bst.print_all()
    print()
    del bst[6]
    del bst[14]
    del bst[13]
    del bst[12]
    del bst[8]
    del bst[9]
    del bst[10]
    del bst[11]
    del bst[7]
    print(bst)
    print(len(bst))
    bst.print_all()
    print(bst._root)
