from collections.abc import MutableMapping
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

    def __init__(self):
        self._root = None
        self._size = 0

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
        insert_idx = self._node24_idx_in_parent(node24)

        # insert node to parent
        upward_node = node24.items.pop(2)
        parent.items.insert(insert_idx, upward_node)

        # form new node24 to save last item in old node24 and its children, also rearrange node24 items and children
        new_node24 = TwoFourTree._Node24()
        new_node24.parent = parent
        new_node24.items.insert(0, node24.items.pop(2))
        new_node24.children.insert(0, node24.children.pop(3))
        new_node24.children.insert(1, node24.children.pop(3))

        parent.children.insert(insert_idx+1, new_node24)
        return parent

    def _node24_idx_in_parent(self, node24):
        for i, item in enumerate(node24.parent.children):
            if item == node24:
                return i

    def _build_map(self, maps):
        pass

    def print_all(self):
        pass

    @staticmethod
    def _key_validation(key):
        hash(key)
        return key


if __name__ == '__main__':
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

    # T1[21] = '21U'
    # T1[100] = '100G'
    # T1[30] = '30I'
    # print(T1)
    # print(N4)
    # T1._split(N4)
    # print(T1)
    # print(N1)
    # print(N4)
    # print(T1[90])
    N1.add_items(12, '12L')
    N1.add_items(19, '19V')
    print(N1)
    print(T1._split(N1))
    print(N1)
    print(T1._root)
