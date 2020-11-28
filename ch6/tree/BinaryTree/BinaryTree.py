import abc
from ch6.tree.Tree.Tree import Tree


class BinaryTree(Tree):
    @abc.abstractmethod
    def left(self, node):
        """Return node's left child node"""

    @abc.abstractmethod
    def right(self, node):
        """Return node's right child node"""

    @abc.abstractmethod
    def _attach_left(self, node, child_node):
        """Attach child node to the left of node"""

    @abc.abstractmethod
    def _attach_right(self, node, child_node):
        """Attach child node to the right of node"""

    def sibling(self, node):
        parent = self.parent(node)
        if parent:
            if node is self.left(parent):
                return self.right(parent)
            return self.left(parent)
        return None

    def children(self, node):
        if self.left(node):
            yield self.left(node)
        if self.right(node):
            yield self.right(node)

    def children_num(self, node):
        left = self.left(node)
        right = self.right(node)
        return 2 if left and right else int(left or right)


if __name__ == '__main__':
    help(BinaryTree.children_num)
