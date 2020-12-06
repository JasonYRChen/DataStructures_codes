from ch9.tree.BinaryTree import BinaryTree
from collections.abc import Iterable
from collections import deque


class MultipleNodesError(Exception):
    pass


class ArrayBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_element', '_key', '_index'

        def __init__(self, key=None, element=None, index=None):
            self._key = key
            self._element = element
            self._index = index

        def __repr__(self):
            return f"Node(k={self._key}, e={self._element}, i={self._index})"

        def __lt__(self, other):
            return self._key < other._key

        def __eq__(self, other):
            return self._key == other._key

    def __init__(self, elements: Iterable = None):
        self._data = []
        self._num_node = 0
        if elements:
            if not isinstance(elements, Iterable):
                raise TypeError('Invalid iterable or sequence.')
            self._build_tree(elements)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"

    def __len__(self):
        return self._num_node

    def key(self, index):
        return self[index]._key

    def set_key(self, index, key):
        self[index]._key = key

    def element(self, index):
        return self[index]._element

    def set_element(self, index, element):
        self[index]._element = element

    def index(self, index):
        return self[index]._index

    def set_index(self, index, new_index):
        self[index]._index = new_index

    def _parent(self, index):
        if index == 0:
            return 0
        return (index - 1) // 2

    def _left(self, index):
        left_index = 2 * index + 1
        if left_index < len(self._data):
            return left_index
        return None

    def _right(self, index):
        right_index = 2 * index + 2
        if right_index < len(self._data):
            return right_index
        return None

    def _add_root(self, key, element):
        if not self._is_empty():
            raise ValueError('Root exists. Cannot add new root')
        self._data.append(self._Node(key, element, 0))
        self._num_node += 1
        return self._data[0]

    def _add_left(self, key, element, index):
        if self[index] is None:
            raise ValueError('Parent node does not exist. Cannot add child node.')
        left_index = self._left(index)
        if left_index and self[left_index] is not None:
            raise ValueError("Left node is occupied. Cannot add new node.")
        if left_index is None:
            left_index = 2 * index + 1
            self._extend_space(left_index)
        self[left_index] = self._Node(key, element, left_index)
        self._num_node += 1
        return self[left_index]

    def _add_right(self, key, element, index):
        if self[index] is None:
            raise ValueError('Parent node does not exist. Cannot add child node.')
        right_index = self._right(index)
        if right_index and self[right_index] is not None:
            raise ValueError("Right node is occupied. Cannot add new node.")
        if right_index is None:
            right_index = 2 * index + 2
            self._extend_space(right_index)
        self[right_index] = self._Node(key, element, right_index)
        self._num_node += 1
        return self[right_index]

    def clear(self):
        """ Clear all nodes in current tree"""
        self._data.clear()
        self._num_node = 0

    def _num_children(self, index):
        return sum(int(self[n] is not None) for n in self._children(index) if n is not None)

    def _delete(self, index):
        if self[index] is None:
            raise ValueError('Node does not exist. Cannot delete node.')
        key, element = self.key(index), self.element(index)
        num_children = self._num_children(index)
        if num_children == 2:
            raise MultipleNodesError('More than one child detect, cannot delete the node.')

        self[index] = None
        if num_children == 1:
            child_idx = self._left(index) if self._data[self._left(index)] else self._right(index)
            self[index], self[child_idx] = self[child_idx], None
            stack = deque([(index, child_idx)])

            while stack:
                curr_idx, prev_idx = stack.popleft()
                for child_idx in self._children(prev_idx):
                    new_child_idx = 2 * curr_idx + 1 if child_idx % 2 else 2 * curr_idx + 2
                    self[new_child_idx], self[child_idx] = self[child_idx], None
                    stack.append((new_child_idx, child_idx))
                self.set_index(curr_idx, curr_idx)
        self._num_node -= 1
        return key, element

    def delete(self, index):
        return self._delete(index)

    def _is_empty(self):
        return len(self) == 0

    def _is_leaf(self, index):
        return self._num_children(index) == 0

    def _is_root(self, index):
        return self[index]._index == 0

    def _replace(self, index, key, element):
        self.set_element(index, element)
        if key is not None:
            self.set_key(index, key)

    def replace(self, index, element, key=None):
        self._replace(index, key, element)

    def _root(self):
        return 0

    def _extend_space(self, index):
        curr_len = len(self._data)
        self._data.extend([None] * (index + 1 - curr_len))

    def _preorder(self, index):
        yield index
        for child_idx in self._children(index):
            if child_idx and self[child_idx] is not None:
                yield from self._preorder(child_idx)

    def _postorder(self, index):
        if not self._is_leaf(index):
            for child_idx in self._children(index):
                yield from self._postorder(child_idx)
        yield index

    def _breadth_first(self, index):
        dq = deque([index])
        while dq:
            index = dq.popleft()
            yield index
            dq.extend(self._children(index))

    def _inorder(self, index):
        left_idx = self._left(index)
        if left_idx and self[left_idx] is not None:
            yield from self._inorder(left_idx)
        yield index
        right_idx = self._right(index)
        if right_idx and self[right_idx] is not None:
            yield from self._inorder(right_idx)

    def preorder(self, index=0):
        """ Give a preorder traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        yield from self._preorder(index)

    def postorder(self, index=0):
        """ Give a postorder traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        yield from self._postorder(index)

    def breadth_first(self, index=0):
        """ Give a breadth-first traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        yield from self._breadth_first(index)

    def inorder(self, index=0):
        """ Give a inorder traversal starting from node

            :param
                node: _Node, if node is None, root node will be applied

            :return generator of node traversal
        """
        yield from self._inorder(index)

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
        for index in self.iter_all(traversal):
            d = self.depth(index)
            print(' ' * indent * d, self._data[index], sep='')

    def _build_tree(self, iterables):
        if not isinstance(iterables, Iterable):
            raise TypeError('Invalid iterable. Elements should be bound into an iterable.')
        if not self._is_empty():
            raise ValueError('Tree already exists. Cannot form a new tree.')
        for i, (key, element) in enumerate(iterables):
            self._data.append(self._Node(key, element, i))
            self._num_node += 1

    def _depth(self, index):
        if index == 0:
            return 0
        return 1 + self._depth(self._parent(index))

    def depth(self, index=0):
        return self._depth(index)

    def _height(self, index):
        if self._is_leaf(index):
            return 0
        return 1 + max(self._height(child_idx) for child_idx in self._children(index))

    def height(self, index=0):
        return self._height(index)


if __name__ == '__main__':
    rank = (4, 'Ian'), (1, 'Jason'), (3, 'Ryan'), (2, 'Shawn'), (5, 'Chris'), (8, 'Nick'), (11, 'Bob'), (7, 'Rick'), (13, 'Wu')
    t = ArrayBinaryTree(rank)
    print(t._data)
    print('length:', len(t), 'height:', t.height())
    t.list_all()
    t.delete(4)
    # t.delete(1)
    t._add_right(100, 'Keyman', 7)
    print(t._data)
    print('length:', len(t), 'height:', t.height())
    t.list_all()
    # t.clear()
    # t._add_root(300, 'Word')
    # print(t._data)
    # print('length:', len(t), 'height:', t.height())
    # t.list_all()

