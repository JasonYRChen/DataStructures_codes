from ch9.tree.BaseTree import BaseTree
from abc import abstractmethod


class BinaryTree(BaseTree):
    @abstractmethod
    def _left(self, node):
        """ Return node's left child node

            :param
                node: user defined or list element

            :return node
        """

    @abstractmethod
    def _right(self, node):
        """ Return node's right child node

            :param
                node: user defined or list element

            :return node
        """

    @abstractmethod
    def _add_left(self, node, element):
        """ Add a new node to the node with element

            :param
                node: user defined or list element
                element: any type of instance

            :return node, child node
        """

    @abstractmethod
    def _add_right(self, node, element):
        """ Add a new node to the node with element

            :param
                node: user defined or list element
                element: any type of instance

            :return node, child node
        """

    def _attach(self, tree, node):
        """ Attach another tree to designated node on current tree

            :param
                tree: a binary tree type, or iterable ready to form a binary tree
                node: user defined or list element

            :return None or current tree
        """
        raise NotImplementedError

    def _detach(self, node):
        """ Detach certain node and nodes beyond the node from current tree.

            :param
                node: user defined or list element

            :return None or detached tree or node
        """
        raise NotImplementedError

    def _children(self, node):
        if self._left(node) is not None:
            yield self._left(node)
        if self._right(node) is not None:
            yield self._right(node)

    def _num_children(self, node):
        return sum(int(n is not None) for n in self._children(node))

    def _sibling(self, node):
        if self._is_root(node):
            return None

        parent = self._parent(node)
        return self._left(parent) if node is self._right(parent) else self._right(parent)
