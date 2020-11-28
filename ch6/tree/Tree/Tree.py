import abc


class Tree(abc.ABC):
    @abc.abstractmethod
    def __len__(self):
        """Total node numbers"""

    def __repr__(self):
        return f"{self.__class__.__name__}(node_numbers: {len(self)})"

    @abc.abstractmethod
    def root(self):
        """Return root node"""

    def is_root(self, node):
        """Check if node is the root node."""
        return self.parent(node) is None

    @abc.abstractmethod
    def parent(self, node):
        """Return node's parent node"""

    def children(self, node):
        """Iterate node's children."""
        raise NotImplementedError

    def children_num(self, node):
        """Return numbers of children"""
        raise NotImplementedError

    @abc.abstractmethod
    def element(self, node):
        """Return node's element"""

    def is_leaf(self, node):
        return self.children_num(node) == 0

    @abc.abstractmethod
    def attach(self, node, *nodes):
        """Attach new nodes or None to current node"""

    @abc.abstractmethod
    def detach(self, node):
        """Remove the node and connect its children to its parent if legitimate."""

    @abc.abstractmethod
    def _replace(self, node, elements):
        """Replace elements in the node."""

    @abc.abstractmethod
    def _disable_node(self, node):
        """Make node invalid and reduce total nodes number by 1.
        May accompany with self.detach method."""

    @abc.abstractmethod
    def _add_root(self, node=None):
        """Add root to the tree"""

    def height(self, node=None):
        """Height is zero-base, starts from current node.
        Ex: node's height is 0, node's children's height is 1, and so on)."""

        if node is None:
            node = self.root()
        if self.is_leaf(node):
            return 0
        return 1 + max(self.height(c) for c in self.children(node))

    def depth(self, node):
        """Depth is zero-base, starts from root node"""
        if node is self.root():
            return 0
        return 1 + self.depth(self.parent(node))
