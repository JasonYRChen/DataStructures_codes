from ch6.tree.BinaryTree.BinaryTree import BinaryTree


class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_elements', '_parent', '_left', '_right'

        def __init__(self, element=None, parent=None, left=None, right=None):
            self._elements = element
            self._parent = parent
            self._left = left
            self._right = right

    def __init__(self, obj=None):
        self._size = 0
        self._dummy_root = self._Node()
        self._dummy_root._right = self._dummy_root._left
        if obj is not None:
            self._add_root(obj)

    def __len__(self):
        return self._size

    def _make_node(self, obj):
        """Given valid obj (tree or node), return length of obj and node itself or its root."""
        if isinstance(obj, self.__class__):
            return len(obj), obj._dummy_root._left
        elif isinstance(obj, self.__class__._Node):
            return 1, obj
        else:
            return 1, self._Node(obj)

    def _valid_node(self, node):
        if not isinstance(node, self._Node):
            raise TypeError('Invalid node type.')
        if node._parent is node:
            raise ValueError('This node is no longer valid.')
        return node

    def _add_root(self, obj):
        size, node = self._make_node(obj)
        if self._dummy_root._left is not None:
            raise ValueError('Root already exists, cannot add new root.')
        self._dummy_root._left, node._parent = node, self._dummy_root
        self._size += size

    def root(self):
        return self._dummy_root._left

    def parent(self, node):
        node = self._valid_node(node)
        return node._parent

    def element(self, node):
        node = self._valid_node(node)
        return node._elements

    def left(self, node):
        node = self._valid_node(node)
        return node._left

    def right(self, node):
        node = self._valid_node(node)
        return node._right

    def attach_left(self, node, obj):
        node = self._valid_node(node)
        if node._left is not None:
            raise ValueError(f'Node {node} already has left node {node._left}. Cannot attach new node')
        size, child_node = self._make_node(obj)
        node._left = child_node
        child_node._parent = node
        self._size += size

    def attach_right(self, node, obj):
        node = self._valid_node(node)
        if node._right:
            raise ValueError(f'Node {node} already has left node {node._right}. Cannot attach new node')
        size, child_node = self._make_node(obj)
        node._right = child_node
        child_node._parent = node
        self._size += size

    def _replace(self, node, elements):
        node = self._valid_node(node)
        node._elements = elements

    def _disable_node(self, node):
        node._parent = node
        node._left = node._right = None

    def detach(self, node):
        node = self._valid_node(node)
        if self.children_num(node) == 2:
            raise ValueError(f"Detach failed. {node} has 2 children. Cannot attach both children to its parent node.")

        parent = node._parent
        child = node._left if node._left is not None else node._right
        if parent._left is node:
            parent._left = child
        else:
            parent._right = child
        if child is not None:
            child._parent = parent
        self._disable_node(node)
        self._size -= 1


if __name__ == '__main__':
    t = LinkedBinaryTree()
    print(dir(t))