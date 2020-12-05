from ch9.tree.BinaryTree import BinaryTree
from collections.abc import Iterable
from math import ceil, log2
from collections import deque


class MultipleNodesError(Exception):
    pass


class ArrayBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_element', '_index'

        def __init__(self, index=None, element=None):
            self._index = index
            self._element = element

        def __repr__(self):
            return f"Node(index={self._index}, element={self._element})"

        def __lt__(self, other):
            return self._element < other._element

        def __eq__(self, other):
            return self._element == other._element

    def __init__(self, elements: Iterable = None):
        self._data = []
        self._size = 0  # the maximum space for a complete tree
        self._num_node = 0
        if elements:
            if not isinstance(elements, Iterable):
                raise TypeError('Not a valid sequence.')
            self._build_tree(elements)

    def __getitem__(self, index):
        return self._data[index]

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"

    def __len__(self):
        return self._num_node

    @staticmethod
    def index(node):
        return node._index

    @staticmethod
    def _set_index(node, index):
        node._index = index

    @staticmethod
    def element(node):
        return node._element

    @staticmethod
    def _set_element(node, element):
        node._element = element

    def _parent(self, node):
        index = self.index(node)
        if index == 0:
            return None
        return self[(index - 1) // 2]

    def parent(self, node):
        return self._parent(node)

    def _left(self, node):
        index = self.index(node)
        left_index = 2 * index + 1
        if left_index < self._size:
            return self[left_index]
        return None

    def _right(self, node):
        index = self.index(node)
        left_index = 2 * index + 2
        if left_index < self._size:
            return self[left_index]
        return None

    def _add_root(self, element):
        if not self._is_empty():
            raise ValueError('Root exists. Cannot add new root')
        self._data.append(self._Node(element, 0))
        self._size = 1
        self._num_node = 1

    def _add_left(self, node, element):
        if self._left(node) is not None:
            raise ValueError("Left node is occupied. Cannot add new node.")
        index = self.index(node)
        child_index = 2 * index + 1
        if child_index >= self._size:
            self._extend_space()
        self._data[child_index] = self._Node(element, child_index)
        self._num_node += 1

    def _add_right(self, node, element):
        if self._right(node) is not None:
            raise ValueError("Right node is occupied. Cannot add new node.")
        index = self.index(node)
        child_index = 2 * index + 2
        if child_index > self._size:
            self._extend_space()
        self._data[child_index] = self._Node(element, child_index)
        self._num_node += 1

    def _clear(self):
        """ Clear all nodes in current tree"""
        self._data.clear()
        self._size = 0
        self._num_node = 0

    def clear(self):
        self._clear()

    def _delete(self, node):
        index, element = self.index(node), self.element(node)
        if self._num_children(node) == 2:
            raise MultipleNodesError('More than one child detect, cannot delete the node.')

        try:
            child = next(self._children(node))
        except StopIteration:
            child = None
        else:
            self._data[self.index(child)] = None
        self._set_index(node, -1)
        self._data[index] = child
        stack = deque([(index, child)]) if child is not None else deque()
        while stack:
            index, node = stack.popleft()
            for child in self._children(node):
                curr_child_idx = self.index(child)
                new_child_idx = 2 * index + 1 if curr_child_idx % 2 else 2 * index + 2
                self._data[new_child_idx], self._data[curr_child_idx] = child, None
                stack.append((new_child_idx, child))
            self._set_index(node, index)
        self._num_node -= 1
        return element

    def delete(self, node):
        return self._delete(node)

    def _is_empty(self):
        return len(self) == 0

    def _is_leaf(self, node):
        return self._num_children(node) == 0

    def _is_root(self, node):
        return node._index == 0

    def _replace(self, node, element):
        self._set_element(node, element)

    def replace(self, node, element):
        return self._replace(node, element)

    def _root(self):
        return self[0]

    def _extend_space(self):
        """ Extend current tree array with maximum next level children numbers"""
        h = log2(self._size + 1) - 1
        new_length = int(2 ** (h+2) - 1)
        self._data.extend([None] * (new_length - self._size))
        self._size = new_length

    def _preorder(self, node):
        yield node
        for child in self._children(node):
            if child is not None:
                yield from self._preorder(child)

    def _postorder(self, node):
        if not self._is_leaf(node):
            for child in self._children(node):
                yield from self._postorder(child)
        yield node

    def _breadth_first(self, node):
        dq = deque([node])
        while dq:
            node = dq.popleft()
            yield node
            dq.extend(self._children(node))

    def _inorder(self, node):
        if self._left(node) is not None:
            yield from self._inorder(self._left(node))
        yield node
        if self._right(node) is not None:
            yield from self._inorder(self._right(node))

    def preorder(self, node=None):
        """ Give a preorder traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        if node is None:
            node = self._root()
        yield from self._preorder(node)

    def postorder(self, node=None):
        """ Give a postorder traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        if node is None:
            node = self._root()
        yield from self._postorder(node)

    def breadth_first(self, node=None):
        """ Give a breadth-first traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        if node is None:
            node = self._root()
        yield from self._breadth_first(node)

    def inorder(self, node=None):
        """ Give a inorder traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        if node is None:
            node = self._root()
        yield from self._inorder(node)

    def iter_all(self, traversal=None):
        """ Iterate all the nodes in current tree in generator. Designate tree traversal
            method to iter all nodes.

            :param
                traversal: traversal method, including 'preorder', 'postorder', 'inorder', and
                            'breadth-first'. 'breadth-first' is default traversal method.
        """
        if traversal is None:
            traversal = self.breadth_first
        yield from traversal()

    def list_all(self, traversal=None, indent=2):
        """ Print the tree with designated traversal method

            :param
                traversal: traversal method, including 'preorder', 'postorder', 'inorder', and
                            'breadth-first'. 'preorder' is default traversal method.
                indent: the indent of printed node corresponds to respective height
        """
        if traversal is None:
            traversal = self.preorder
        for node in self.iter_all(traversal):
            d = self.depth(node)
            print(' ' * indent * d, node, sep='')

    def _build_tree(self, iterables):
        if not isinstance(iterables, Iterable):
            raise TypeError('Invalid iterable. Elements should be bound into an iterable.')
        for i, element in enumerate(iterables):
            if self._is_empty():
                self._add_root(element)
            else:
                if i == self._size:
                    self._extend_space()
                self._data[i] = self._Node(element, i)
                self._num_node += 1

    def depth(self, node):
        index = self.index(node)
        if index == 0:
            return 0
        return 1 + self.depth(self._parent(node))

    def _height(self, node):
        if self._is_leaf(node):
            return 0
        return 1 + max(self._height(child) for child in self._children(node))

    def height(self, node=None):
        if node is None:
            node = self._root()
        return self._height(node)


if __name__ == '__main__':
    # t = ArrayBinaryTree(range(13))
    # print(t._data)
    # print('length:', len(t))
    # print(t._data)
    # t.list_all(t.preorder)
    # print()
    # print(t._data)
    # print(t.delete(t[12]))
    # print(t._data)
    # print(t.delete(t[5]))
    # print(t._data)
    # print(t.delete(t[5]))
    # print(t._data)
    # print('length:', len(t))
    # t.list_all(t.preorder)
    #
    # print()
    # print(t.delete(t[2]))
    # print(t.delete(t[2]))
    # print(t.delete(t[0]))
    # print('length:', len(t))
    # print(t._data)
    # t.list_all(t.preorder)

    t = ArrayBinaryTree(range(5))
    print(t)
    print('length:', len(t))
    t.list_all(t.preorder)
    print()
    t._add_right(t[2], 100)
    print(t)
    print('length:', len(t))
    t.list_all(t.preorder)
    print()
    t._add_right(t[4], 100)
    print(t)
    print('length:', len(t))
    t.list_all(t.preorder)
