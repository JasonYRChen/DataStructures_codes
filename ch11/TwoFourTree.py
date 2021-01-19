from collections.abc import MutableMapping, Mapping
from itertools import zip_longest


class TwoFourTree(MutableMapping):
    class _Node:
        __slots__ = 'key', 'value'

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __repr__(self):
            return f"{self.key}={self.value}"

        def __lt__(self, other):
            return self.key < other

        def __gt__(self, other):
            return self.key > other

        def __eq__(self, other):
            return self.key == other

    class _Node24:
        __slots__ = 'items', 'parent', 'children'

        def __init__(self, items=None, parent=None, children=None):
            self.items = TwoFourTree._List(4)
            self.parent = parent
            self.children = TwoFourTree._List(5)
            if items:
                for i, item in enumerate(items):
                    self.items[i] = item
            if children:
                for i, child in children:
                    self.children[i] = child

        def __repr__(self):
            return f"Node24(items={self.items}, parent={self.parent.items if self.parent else None}, children={self.children})"

        def __len__(self):
            return len(self.items)

        def __iter__(self):
            yield from self.items

        def __getitem__(self, idx):
            return self.items[idx]

        def add_items(self, key, value):
            idx = len(self)
            self.items[idx] = TwoFourTree._Node(key, value)
            self.items.sort()

        def is_leaf(self):
            return not any(self.children)

    class _List:
        __slots__ = 'list'

        def __init__(self, blank):
            self.list = [None] * blank

        def __repr__(self):
            return f"{self.list}"

        def __len__(self):
            count = 0
            for item in self.list:
                if item is not None:
                    count += 1
                else:
                    break
            return count

        def __getitem__(self, idx):
            return self.list[idx]

        def __setitem__(self, idx, node24):
            self.list[idx] = node24

        def __iter__(self):
            for item in self.list:
                if item:
                    yield item

        def sort(self):
            num = len(self)
            sort = sorted(self.list[:num])
            self.list[:num] = sort

        def insert(self, index, node):
            last_idx = len(self) - 1
            while last_idx >= index:
                self[last_idx+1] = self[last_idx]
                last_idx -= 1
            self[index] = node

        def pop(self, index):
            node = self[index]
            last_idx = len(self) - 1
            while index < last_idx:
                self[index] = self[index+1]
                index += 1
            self[index] = None
            return node

        def index(self, target):
            for i, item in enumerate(self.list):
                if item == target:
                    return i
            return None

        def is_empty(self):
            return not any(self.list)

    def __init__(self, maps=None):
        self._root = self._Node24()
        self._size = 0
        if maps:
            self._build_map(maps)

    def __getitem__(self, key):
        key = self._key_validation(key)
        node, _ = self._search(key, self._root)
        if node is None:
            raise KeyError(f'Invalid key {key}')
        return node.value

    def __setitem__(self, key, value):
        key = self._key_validation(key)
        node, node24 = self._search(key, self._root)
        if node:
            node.value = value
        else:
            self._size += 1
            node24.add_items(key, value)
            self._split_iter(node24)

    def __delitem__(self, key):
        key = self._key_validation(key)
        node, node24 = self._search(key, self._root)
        if node is None:
            raise KeyError(f'Invalid key {key}')

        leaf_node24, index = self._before(node24, node)
        del_node = node24.items.pop(node24.items.index(node))
        self._size -= 1
        # always move the blank to the leaf
        if not node24.is_leaf():
            self._transfer(index, leaf_node24, node24)
            node24 = leaf_node24

        if node24.items.is_empty() and node24 != self._root:
            self._parent2child(node24)  # transfer item from parent to child
            sibling, right = self._siblings(node24)
            if len(sibling.items) > 1:
                self._sibling2parent(sibling, right)  # transfer item from sibling to parent
            else:
                # parent = node24.parent
                while node24 != self._root and len(node24.parent.items) < len(node24.parent.children) - 1:
                    sibling, right = self._siblings(node24)
                    to_fuse, be_fused = (node24, sibling) if right else (sibling, node24)
                    fused = self._fuse(to_fuse, be_fused)
                    # fusion
                    parent = fused.parent
                    parent.children.pop(parent.children.index(be_fused))
                    self._split_iter(fused)  # make sure split happen if fused's items number reach to 4

                    if parent == self._root and parent.items.is_empty():
                        self._root = fused
                        break
                    if parent.items.is_empty():
                        self._parent2child(parent)

                    node24 = parent
        return del_node.value

    def __repr__(self):
        content = ', '.join(repr(node) for node in self._sequential_yield(self._root))
        return f"{self.__class__.__name__}({content})"

    def __iter__(self):
        for node in self._sequential_yield(self._root):
            yield node.key

    def __len__(self):
        return self._size

    def _sequential_yield(self, node24):
        """
        This generator yield node in key's ascending form, offering inorder-like traversal
        """
        for child, node in zip_longest(node24.children, node24.items):
            if child:
                yield from self._sequential_yield(child)
            if node:
                yield node

    def _search(self, key, node24):
        if node24 is None:
            return None,
        for i, node in enumerate(node24):
            if key == node:
                return node, node24
            if key < node or i == len(node24) - 1:
                i = i if key < node else i + 1
                result = self._search(key, node24.children[i])
                if len(result) == 1:
                    return None, node24
                return result
        return None, node24  # should only be reached by root configuration

    def _split_iter(self, node24):
        if len(node24) == 4:
            node24 = self._split(node24)
            self._split_iter(node24)
        return

    def _split(self, node24):
        parent = node24.parent
        if parent is None:
            parent = TwoFourTree._Node24()
            self._root, parent.children[0], node24.parent = parent, node24, parent
        insert_idx = node24.parent.children.index(node24)

        # insert node to parent
        upward_node = node24.items.pop(2)
        parent.items.insert(insert_idx, upward_node)

        # form new node24 to save last item in old node24 and its children, also rearrange node24 items and children
        new_node24 = TwoFourTree._Node24()
        new_node24.parent = parent
        new_node24.items.insert(0, node24.items.pop(2))
        new_node24.children.insert(0, node24.children.pop(3))
        new_node24.children.insert(1, node24.children.pop(3))
        for child in new_node24.children:
            if child:
                child.parent = new_node24
            else:
                break

        parent.children.insert(insert_idx+1, new_node24)
        return parent

    def _build_map(self, maps):
        if isinstance(maps, Mapping):
            maps = maps.items()
        for key, value in maps:
            self[key] = value

    def print_all(self, rate=4):
        for level, item in self._print_all(self._root, 0):
            print(' ' * level * rate, item, sep='')

    def _print_all(self, node24, level):
        yield level, node24.items
        for child in node24.children:
            if child:
                yield from self._print_all(child, level+1)

    @staticmethod
    def _key_validation(key):
        hash(key)
        return key

    def _transfer(self, index, from_node24, to_node24):
        node = from_node24.items.pop(index)
        to_node24.add_items(node.key, node.value)

    def _fuse(self, to_fuse, be_fused):
        # Caution: To use this method, to_fuse node24 should always be on the left of be_fused node24
        for node in be_fused.items:
            to_fuse.add_items(node.key, node.value)

        index = len(to_fuse.children)
        for node24 in be_fused.children:
            node24.parent = to_fuse
            to_fuse.children.insert(index, node24)
            index += 1
        return to_fuse

    def _before(self, node24, node):
        index = node24.items.index(node)
        while not node24.is_leaf():
            node24 = node24.children[index]
            index = len(node24.children) - 1
        return node24, len(node24.items) - 1

    def _siblings(self, node24):
        # The second returned value indicates the sibling is on the left or right of node24
        parent = node24.parent
        index = parent.children.index(node24)
        if index == len(parent.children) - 1:
            return parent.children[index-1], False
        else:
            return parent.children[index+1], True

    def _sibling2parent(self, sibling, right=True):
        parent = sibling.parent
        if right:
            self._transfer(0, sibling, parent)
        else:
            self._transfer(len(sibling.items) - 1, sibling, parent)
        return sibling

    def _parent2child(self, node24):
        parent = node24.parent
        index = parent.children.index(node24)
        if index == len(parent.items):
            index -= 1
        self._transfer(index, parent, node24)


if __name__ == '__main__':
    from string import ascii_letters as al

    node = TwoFourTree._Node
    ls = TwoFourTree._List
    node24 = TwoFourTree._Node24

    N1 = node24()
    N2 = node24()
    N3 = node24()
    N4 = node24()

    N1.items[0] = node(10, '10A')
    N1.items[1] = node(20, '20B')
    N2.items[0] = node(5, '5E')
    N2.items[1] = node(8, '8h')
    N3.items[0] = node(11, '11K')
    N3.items[1] = node(15, '15O')
    N4.items[0] = node(23, '23W')

    T1 = TwoFourTree()
    T1._root = N1

    for i, Node in enumerate([N2, N3, N4]):
        N1.children[i] = Node
        Node.parent = N1

    a = [(10, 'k'), (4, 'e'), (12, 'm'), (7, 'h'), (1, 'b'), (9, 'j'), (2, 'c'), (11, 'l'), (5, 'f'), (8, 'i'), (3, 'd'), (6, 'g'), (0, 'a')]
    b = [(0, 'a'), (1, 'b'), (12, 'm'), (4, 'e'), (6, 'g'), (9, 'j'), (3, 'd'), (14, 'o'), (19, 't'), (10, 'k'), (7, 'h'), (13, 'n'), (18, 's'), (15, 'p'), (16, 'q'), (8, 'i'), (5, 'f'), (11, 'l'), (2, 'c'), (17, 'r')]
    # T2 = TwoFourTree()
    # for i, char in a:
    #     T2[i] = char
    T2 = TwoFourTree(b)
    print(T2)
    print('len:', len(T2))
    print(T2._root)
    T2.print_all()

    to_del = [6, 3, 2, 9, 12]
    # to_del = [12]
    for key in to_del:
        del T2[key]
        print(T2)
        print('len:', len(T2))
        print(T2._root)
        T2.print_all()
    T2[7.7] = '7.7'
    T2[7.8] = '7.8'
    print(T2)
    print('len:', len(T2))
    print(T2._root)
    T2.print_all()
