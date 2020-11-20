from collections.abc import Sequence


class DoublyLinkedNode:
    __slots__ = '_val', '_prev', '_next'

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
        for _ in range(len(self)):
            items.append(node._val)
            node = node._next
        return f"{self.__class__.__name__}({items})"

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        if item < 0:
            item += len(self)
        if not 0 <= item < len(self):
            raise IndexError('Invalid index.')

        node = self._head
        for _ in range(item):
            node = node._next
        return node._val

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
        for _ in range(len(self)):
            print(node)
            node = node._next

    def append(self, item):
        if self._head is None:
            self._head, self._tail = self._build_nodes([item])
        else:
            self._tail._next = DoublyLinkedNode(item, self._tail, self._head)
            self._head._prev, self._tail = self._tail._next, self._tail._next
            self._size += 1

    def appendleft(self, item):
        if self._head is None:
            self._head, self._tail = self._build_nodes([item])
        else:
            self._head._prev = DoublyLinkedNode(item, self._tail, self._head)
            self._tail._next, self._head = self._head._prev, self._head._prev
            self._size += 1

    def pop(self):
        if self._head is None:
            raise ValueError('Empty deque.')

        item = self._tail._val
        if len(self) == 1:
            self._head = self._tail = None
        else:
            self._tail._prev._next, self._tail._next._prev = self._tail._next, self._tail._prev
            self._tail = self._tail._prev
        self._size -= 1
        return item

    def popleft(self):
        if self._head is None:
            raise ValueError('Empty deque.')

        item = self._head._val
        if len(self) == 1:
            self._head = self._tail = None
        else:
            self._head._next._prev, self._head._prev._next = self._head._prev, self._head._next
            self._head = self._head._next
        self._size -= 1
        return item

    def insert(self, index, item):
        if index < 0:
            index += len(self)
        if len(self) > 0:
            if not 0 <= index < len(self):
                raise IndexError('Invalid index.')

        if len(self) == 0:
            self._head, self._tail = self._build_nodes([item])
        else:
            node = self._head
            for _ in range(index):
                node = node._next
            node._prev = DoublyLinkedNode(item, node._prev, node)
            node._prev._prev._next = node._prev
            if index == 0:
                self._head = node._prev
            self._size += 1

    def remove(self, index):
        if self._head is None:
            raise IndexError('Empty deque.')

        if index < 0:
            index += len(self)
        if not 0 <= index < len(self):
            raise IndexError('Invalid index.')

        if len(self) == 1:
            self._head = self._tail = None
        else:
            node = self._head
            for _ in range(index):
                node = node._next
            node._prev._next, node._next._prev = node._next, node._prev
            if index == 0:
                self._head = node._next
        self._size -= 1

    def rotate(self, shift):
        if shift >= 0:
            for _ in range(shift):
                self._head, self._tail = self._head._next, self._tail._next
        else:
            for _ in range(-shift):
                self._head, self._tail = self._head._prev, self._tail._prev

    def extend(self, iters):
        if self._head is None:
            self._head, self._tail = self._build_nodes(iters)
        else:
            first, tail = self._build_nodes(iters)
            self._tail._next, first._prev = first, self._tail
            self._head._prev, tail._next = tail, self._head
            self._tail = tail

    def extendleft(self, iters):
        if self._head is None:
            self._head, self._tail = self._build_nodes(iters)
        else:
            first, tail = self._build_nodes(iters)
            self._tail._next, first._prev = first, self._tail
            self._head._prev, tail._next = tail, self._head
            self._head = first

    def clear(self):
        self._head = self._tail = None
        self._size = 0

    def count(self, item):
        node = self._head
        num = 0
        for _ in range(len(self)):
            if node._val == item:
                num += 1
            node = node._next
        return num

    def reverse(self):
        node = self._head
        for _ in range(len(self)):
            node._prev, node._next = node._next, node._prev
            node = node._prev
        self._head, self._tail = self._tail, self._head

    def copy(self):
        iters = []
        node = self._head
        for _ in range(len(self)):
            iters.append(node._val)
            node = node._next
        return Deque(iters)


if __name__ == '__main__':
    d = Deque([2, 2, 3, 4])
    print(d.count(1))
    print(d, 'len:', len(d), ', id:', id(d))
    c = d.copy()
    print(c, 'len:', len(c), ', id:', id(c))
    c._list_all()
