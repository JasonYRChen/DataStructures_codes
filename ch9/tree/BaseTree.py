from abc import ABC, abstractmethod


class BaseTree(ABC):
    @abstractmethod
    def __len__(self):
        """ Return numbers of nodes

            :return int
        """

    @abstractmethod
    def _is_empty(self):
        """ Return if tree is empty

            :return bool
        """

    @abstractmethod
    def _root(self):
        """ Return root node

            :return node
        """

    @abstractmethod
    def _is_root(self, node):
        """ Return if node is a root

            :param
                node: user defined or list element

            :return bool
        """

    @abstractmethod
    def _add_root(self, element):
        """ Add root node with element and return root node if necessary

            :param
                element: any type of instance

            :return node
        """

    @abstractmethod
    def _is_leaf(self, node):
        """ Return if node is a leaf

            :param
                node: user defined or list element

            :return bool
        """

    @abstractmethod
    def _parent(self, node):
        """ Return node's parent node

            :param
                node: user defined or list element

            :return node
        """

    @abstractmethod
    def _children(self, node):
        """ Return node's all children nodes in generator form

            :param
                node: user defined or list element

            :return node
        """

    @abstractmethod
    def _num_children(self, node):
        """ Return node's children number

            :param
                node: user defined or list element

            :return int
        """

    @abstractmethod
    def _delete(self, node):
        """ Delete node and return deleted node's element

            :param
                node: user defined or list element

            :return node's element
        """

    @abstractmethod
    def _replace(self, node, element):
        """ Replace node's element with new element

            :param
                node: user defined or list element
                element: any type of instance

            :return None
        """
