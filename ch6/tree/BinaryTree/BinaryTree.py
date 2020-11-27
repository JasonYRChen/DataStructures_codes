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
    def attach_left(self, node, child_node):
        """Attach child node to the left of node"""

    @abc.abstractmethod
    def attach_right(self, node, child_node):
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

    def attach(self, node, left=None, right=None):
        if left:
            self.attach_left(node, left)
        if right:
            self.attach_right(node, right)

    def detach(self, node):
        if self.children_num(node) == 2:
            raise ValueError(f"Detach failed. {node} has 2 children. Cannot attach both children to its parent node.")
        if node is self.root():
            if self.left(node):
                self.add_root(self.left(node))
            else:
                self.add_root(self.right(node))  # self.right(node) may be None.
        else:
            parent = self.parent(node)
            self.attach(parent, self.left(node), self.right(node))
        self.disable_node(node)


if __name__ == '__main__':
    help(BinaryTree.children_num)
