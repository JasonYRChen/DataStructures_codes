from ch11.RedBlackTree.BinarySearchTree import BinarySearchTree


class RedBlackTree(BinarySearchTree):
    class _Node(BinarySearchTree._Node):
        __slots__ = 'red'

        def __init__(self, key=None, value=None, parent=None, left=None, right=None, red=True):
            super().__init__(key, value, parent, left, right)
            self.red = red

        def __repr__(self):
            return f"k={self.key}, v={self.value}, " \
                   f"p={self.parent.key if self.parent else None}, " \
                   f"l={self.left.key if self.left else None}, " \
                   f"r={self.right.key if self.right else None}, " \
                   f"is_red={self.red}"

    def __init__(self, dict_iter=None):
        super().__init__(dict_iter)

    def __setitem__(self, key, value):
        key = self.valid_key(key)
        node = self.search(key, self._root)
        if node is None or key != node.key:
            new_node = self._Node(key, value, node)
            self._size += 1
            if node is None:
                self._reroot(new_node)
                return
            elif key > node.key:
                node.right = new_node
            else:
                node.left = new_node
            self._set_valid_tree(new_node)
        else:
            node.value = value

    def __delitem__(self, key):
        key = self.valid_key(key)
        node = self.search(key, self._root)
        if key != node.key:
            raise KeyError(f"Invalid key '{key}'")
        self._size -= 1
        if not self.is_leaf(node):
            node_before = self.before(node)
            node.key, node.value = node_before.key, node_before.value
            node = node_before

        sibling = self._sibling(node)
        child = node.left if node.left else node.right
        self._relink(child, node.parent, node == node.parent.left if node.parent else None)
        if not node.red:
            self._del_node(sibling)

    def _rotate(self, node):
        p_node, g_node = node.parent, node.parent.parent
        if (p_node.key > node.key > g_node.key) or (p_node.key < node.key < g_node.key):
            is_left = node == p_node.left
            subtree = node.right if is_left else node.left
            self._relink(node, g_node, not is_left)
            self._relink(p_node, node, not is_left)
            self._relink(subtree, p_node, is_left)
            p_node = node
        is_left = p_node == g_node.left
        subtree = p_node.right if is_left else p_node.left
        self._relink(p_node, g_node.parent, g_node == g_node.parent.left if g_node.parent else None)
        self._relink(g_node, p_node, not is_left)
        self._relink(subtree, g_node, is_left)
        return p_node

    def _relink(self, child, parent, left=True):
        if parent and left:
            parent.left = child
        elif parent and not left:
            parent.right = child
        else:
            self._reroot(child)

        if child:
            child.parent = parent

    def _sibling(self, node):
        if self.is_root(node):
            return None
        if node == node.parent.left:
            return node.parent.right
        return node.parent.left

    @staticmethod
    def _children(node):
        yield node.left
        yield node.right

    def _reroot(self, node):
        """
        Set node to root node and make sure it's black
        """
        self._root = node
        node.red = False
        return node

    def _set_recoloring(self, node):
        """
        Recoloring for insert mode
        """
        parent = node.parent
        parent.red = False
        self._sibling(parent).red = False
        parent.parent.red = False if self.is_root(parent.parent) else True
        return parent.parent

    def _set_rotate(self, node):
        """
        Rotation for insert mode
        """
        node = self._rotate(node)
        node.red = False
        for child in self._children(node):
            if child:
                child.red = True
        return node

    def _set_valid_tree(self, node):
        """
        Considering two cases, recoloring and rotation, in insert mode
        """
        if node.parent and node.parent.parent and node.parent.red:
            p_sibling = self._sibling(node.parent)
            if p_sibling and p_sibling.red:
                node = self._set_recoloring(node)
                node = self._set_valid_tree(node)
            else:
                node = self._set_rotate(node)
        return node

    def _del_red_sibling(self, sibling):
        """
        For case if sibling node is red in delete mode
        """
        parent = sibling.parent
        is_left = sibling == parent.left
        subtree = sibling.right if is_left else sibling.left
        self._relink(sibling, parent.parent, parent == parent.parent.left if parent.parent else None)
        self._relink(parent, sibling, not is_left)
        self._relink(subtree, parent, is_left)
        sibling.red = False
        parent.red = True
        return parent.left if is_left else parent.right

    def _del_2nodes(self, sibling):
        """
        For case  if sibling node is black and its children are black or Nones
        """
        parent = sibling.parent
        is_fixed = parent.red
        sibling.red, parent.red = True, False
        return sibling if is_fixed else self._sibling(parent)

    def _del_3nodes(self, sibling):
        """
        For case if sibling node is black and has a red child
        """
        parent = sibling.parent
        parent_color = parent.red
        child = sibling.left if sibling.left and sibling.left.red else sibling.right
        node = self._rotate(child)
        node.red = parent_color
        node.left.red = False
        node.right.red = False
        return node

    def _del_node(self, sibling):
        if sibling.red:
            sibling = self._del_red_sibling(sibling)
            return self._del_node(sibling)

        c1, c2 = [c for c in self._children(sibling)]
        if (c1 and c1.red) or (c2 and c2.red):
            return self._del_3nodes(sibling)

        red_parent = sibling.parent.red
        node = self._del_2nodes(sibling)
        return node if red_parent else self._del_node(node)


if __name__ == '__main__':
    a = [(7, 'h'), (13, 'n'), (14, 'o'), (6, 'g'), (4, 'e'), (12, 'm'), (8, 'i'), (2, 'c'), (5, 'f'), (0, 'a'),
         (3, 'd'), (10, 'k'), (1, 'b'), (9, 'j'), (11, 'l')]
    b = [(4, 4), (7, 7), (12, 12), (15, 15), (3, 3), (5, 5), (14, 14), (18, 18),
         (16, 16), (17, 17)]
    rbt = RedBlackTree(b)
    print(rbt)
    print('len:', len(rbt))
    rbt.print_all()
    del rbt[14]
    print(rbt)
    print('len:', len(rbt))
    rbt.print_all()
