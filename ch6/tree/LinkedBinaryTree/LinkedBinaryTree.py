from ch6.tree.BinaryTree.BinaryTree import BinaryTree
from collections import deque


class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_elements', '_parent', '_left', '_right'

        def __init__(self, element=None, parent=None, left=None, right=None):
            self._elements = element
            self._parent = parent
            self._left = left
            self._right = right

        def __repr__(self):
            parent = None if self._parent is None else self._parent._elements
            left = None if self._left is None else self._left._elements
            right = None if self._right is None else self._right._elements
            return f"Node(element={self._elements}, parent={parent}, left={left}, right={right})"

    def __init__(self, obj=None):
        self._size = 0
        self._dummy_root = self._Node('dummy')
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
            node = self._valid_node(obj)
            return 1, node
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

    def is_root(self, node):
        return self.parent(node) is self._dummy_root

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
            raise ValueError(f'{node} already has left node {node._left}. Cannot attach new node')
        size, child_node = self._make_node(obj)
        node._left = child_node
        child_node._parent = node
        self._size += size
        return child_node

    def attach_right(self, node, obj):
        node = self._valid_node(node)
        if node._right:
            raise ValueError(f'{node} already has right node {node._right}. Cannot attach new node')
        size, child_node = self._make_node(obj)
        node._right = child_node
        child_node._parent = node
        self._size += size
        return child_node

    def attach(self, node, left, right):
        if left is not None:
            _, left = self._make_node(left)
            self.attach_left(node, left)
        if right is not None:
            _, right = self._make_node(right)
            self.attach_right(node, right)
        return node

    def _replace(self, node, elements):
        node = self._valid_node(node)
        node._elements = elements
        return node

    def _disable_node(self, node):
        obj = node._elements
        node._parent = node
        node._left = node._right = None
        return obj

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
        obj = self._disable_node(node)
        self._size -= 1
        return obj

    def _preorder(self, node, level):
        yield level, node
        if node is not None:
            if node._left is not None:
                yield from self._preorder(node._left, level+1)
            if node._right is not None:
                yield from self._preorder(node._right, level+1)

    def _postorder(self, node, level):
        if node is not None:
            if node._left is not None:
                yield from self._preorder(node._left, level+1)
            if node._right is not None:
                yield from self._preorder(node._right, level+1)
        yield level, node

    def _inorder(self, node, level):
        if node._left is not None:
            yield from self._inorder(node._left, level+1)
        yield level, node
        if node._right is not None:
            yield from self._inorder(node._right, level+1)

    def _breadth_first(self, node, level):
        dq = deque([[level, node]])
        while dq:
            lv, nd = dq.popleft()
            yield lv, nd
            for child in self.children(nd):
                dq.append([lv+1, child])

    def preorder(self, node=None, level=0):
        if node is None:
            node = self.root()
        else:
            node = self._valid_node(node)
        yield from self._preorder(node, level)

    def postorder(self, node=None, level=0):
        if node is None:
            node = self.root()
        else:
            node = self._valid_node(node)
        yield from self._postorder(node, level)

    def inorder(self, node=None, level=0):
        if node is None:
            node = self.root()
        else:
            node = self._valid_node(node)
        yield from self._inorder(node, level)

    def breadth_first(self, node=None, level=0):
        if node is None:
            node = self.root()
        else:
            node = self._valid_node(node)
        yield from self._breadth_first(node, level)

    def list_all(self, method=None):
        if method is None:
            method = self.preorder
        for level, node in method(self.root(), 0):
            print(' ' * 4 * level + str(node))


if __name__ == '__main__':
    fail_node = LinkedBinaryTree._Node('failed')
    fail_node._parent = fail_node
    test_node = LinkedBinaryTree._Node('testing')

    t = LinkedBinaryTree('root_t')
    r_left = t.attach_left(t.root(), 'root_left')
    r_right = t.attach_right(t.root(), test_node)
    t.attach_left(r_left, 'left_left')
    t.attach_right(r_left, 'left_right')
    t.attach_left(r_right, 'right_left')
    t.attach_right(r_right, 'right_right')

    u = LinkedBinaryTree('root_u')
    u.attach_left(u.root(), t)

    print(t)
    print(u)
    print()
    t.list_all(t.breadth_first)
    print()
    u.list_all()