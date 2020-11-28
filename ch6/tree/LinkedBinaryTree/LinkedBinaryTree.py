from ch6.tree.BinaryTree.BinaryTree import BinaryTree
from ch6.tree.DoublyLinkedList.DoublyLinkedList import BinaryChildren


class LinkedBinaryTree(BinaryTree):
    def __init__(self, root=None):
        self._size = 0
        self._root = None
        if root:
            self._add_root(root)

    def __len__(self):
        return self._size

    def _add_root(self, node=None):
        if node is not None:
            node = self._valid_node(node)
        self._root = node

    def root(self):
        return self._root

    def parent(self, node):
        node = self._valid_node(node)
        return node._parent

    def element(self, node):
        node = self._valid_node(node)
        return node._elements

    def _attach_left(self, node, child_node):
        node = self._valid_node(node)
        child_node = self._valid_node(child_node)
        if node._left:
            raise ValueError(f'Node {node} already has left node {node._left}. Cannot attach new node')
        node._left = child_node
        child_node._parent = node

    def _attach_right(self, node, child_node):
        node = self._valid_node(node)
        child_node = self._valid_node(child_node)
        if node._right:
            raise ValueError(f'Node {node} already has left node {node._right}. Cannot attach new node')
        node._right = child_node
        child_node._parent = node

    def _replace(self, node, elements):
        node = self._valid_node(node)
        node._elements = elements

    def _disable_node(self, node):
        node = self._valid_node(node)
        node._parent = node
        node._left = node._right = None

    def left(self, node):
        node = self._valid_node(node)
        return node._left

    def right(self, node):
        node = self._valid_node(node)
        return node._right

    def attach(self, node, left=None, right=None):
        if left and self._valid_node(left):
            self._attach_left(node, left)
        if right and self._valid_node(right):
            self._attach_right(node, right)

    def detach(self, node):
        if self._valid_node(node):
            if self.children_num(node) == 2:
                raise ValueError(f"Detach failed. {node} has 2 children. Cannot attach both children to its parent node.")
            if node is self.root():
                if self.left(node):
                    self._add_root(self.left(node))
                else:
                    self._add_root(self.right(node))  # self.right(node) may be None.
            else:
                parent = self.parent(node)
                self.attach(parent, self.left(node), self.right(node))
            self._disable_node(node)

    def _valid_node(self, node, node_cls=BinaryChildren):
        if not isinstance(node, node_cls):
            raise TypeError(f'Invalid node type. Node type should be {node_cls}, but {type(node)} instead.')
        if node._parent is node:
            raise ValueError('Invalid node. This node has been dumped.')
        return node


if __name__ == '__main__':
    t = LinkedBinaryTree()
    print(t)