class HuffmanTree:
    class _Node:
        __slots__ = 'key', 'value', 'parent', 'left', 'right'

        def __init__(self, key=None, value=None, parent=None, left=None, right=None):
            self.key = key
            self.value = value
            self.parent = parent
            self.left = left
            self.right = right

        def __repr__(self):
            return f"Node(k={self.key}, v={self.value}, " \
                   f"p={(self.parent.key, self.parent.value) if self.parent else None}, " \
                   f"l={(self.left.key, self.left.value) if self.left else None}, " \
                   f"r={(self.right.key, self.right.value) if self.right else None})"

    def __init__(self, char=None, freq=None):
        self.root = None
        if self.root is None and char is not None and freq is not None:
            self.root = self._Node(freq, char)

    def __repr__(self):
        return f"{self.__class__.__name__}(k={self.root.key}, v={self.root.value})"

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Both instance should be instance of Huffman Tree.")

        new_tree = HuffmanTree()
        new_node = self._Node(self.root.key + other.root.key)
        self._connect(self.root, new_node, True)
        self._connect(other.root, new_node, False)
        new_tree.root = new_node
        return new_tree

    def _connect(self, child, parent, is_left):
        if parent:
            if is_left:
                parent.left = child
            else:
                parent.right = child
        if child:
            child.parent = parent

    def key(self):
        return self.root.key

    @staticmethod
    def is_leaf(node):
        return node.left is None and node.right is None

    @staticmethod
    def left(node):
        return node.left

    @staticmethod
    def right(node):
        return node.right

    def _preorder_traversal(self, node, level):
        yield node, level
        if node.left:
            yield from self._preorder_traversal(node.left, level+1)
        if node.right:
            yield from self._preorder_traversal(node.right, level+1)

    def show_hierarchy(self):
        for node, level in self._preorder_traversal(self.root, 0):
            print(' ' * 4 * level, node, sep='')


if __name__ == '__main__':
    n1 = HuffmanTree._Node(1, 1)
    n2 = HuffmanTree._Node(2, 2)
    n3 = HuffmanTree._Node(3, 3)
    n4 = HuffmanTree._Node(4, 4)

    # n2.left, n2.right, n3.right = n1, n3, n4
    # ht = HuffmanTree()
    # ht.root = n2
    # print(type(ht))
    # ht.show_hierarchy()

    h1 = HuffmanTree('a', 1)
    h2 = HuffmanTree('p', 2)
    h3 = HuffmanTree('l', 1)
    h4 = HuffmanTree('e', 1)

    h = h1 + h2 + h3 + h4
    print(h)
    # print(h.root)
    # h.show_hierarchy()
    print(h1.is_leaf(h1.root))
