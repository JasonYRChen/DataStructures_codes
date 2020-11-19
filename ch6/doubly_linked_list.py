from collections import Sequence


class DoublyLinkedNode:
    def __init__(self, val=0, prev_node=None, next_node=None):
        self._val = val
        self._prev = prev_node
        self._next = next_node

    def __repr__(self):
        return f"{self.__class__.__name__}(val={self._val}, prev={self._prev._val}, next={self._next._val})"


class Deque:
    def __init__(self, iters=None):
        self._head = None
        self._tail = None
        self._size = 0
        if iters:
            self._head, self._tail = self._build_nodes(iters)

    def __repr__(self):
        node, items = self._head, []
        for _ in range(self._size):
            items.append(node._val)
            node = node._next
        return f"{self.__class__.__name__}({items})"

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        pass

    def _build_nodes(self, iters):
        """Build nodes according to iters an return the first and the last nodes. Remember to update self._size"""
        if not isinstance(iters, Sequence):
            raise ValueError('Invalid sequence.')

        first = None
        for item in iters:
            if first is None:
                node = DoublyLinkedNode(item)
                first = node
            else:
                node._val = item
                node._prev = prev
            node._next = DoublyLinkedNode()
            prev, node = node, node._next
            self._size += 1
        prev._next, first._prev = first, prev
        return first, prev

    def _list_all(self):
        node = self._head
        for _ in range(self._size):
            print(node)
            node = node._next

    def append(self, item):
        pass

    def appendleft(self, item):
        pass

    def pop(self):
        pass

    def popleft(self):
        pass

    def insert(self, index, item):
        pass

    def remove(self, index):
        pass

    def rotate(self, shift):
        pass

    def extend(self, iters):
        pass

    def extendleft(self, iters):
        pass

    def clear(self):
        pass

    def count(self, item):
        pass

    def reverse(self):
        pass

    def copy(self):
        pass


if __name__ == '__main__':
    d = Deque(range(5))
    d._list_all()
    print(d)
    print(len(d))