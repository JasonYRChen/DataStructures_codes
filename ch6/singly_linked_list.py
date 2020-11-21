class SinglyLinkedNode:
    __slots__ = '_val', '_next'

    def __init__(self, val=0, next_node=None):
        self._val = val
        self._next = next_node

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._val}, next={self._next._val if self._next else None})"


class SinglyLinkedList:
    def __init__(self):
        self._head = None
        self._size = 0

    def __repr__(self):
        return f"{self.__class__.__name__}(head={self._head}, size={self._size})"

    def __getitem__(self, item):
        if item < 0:
            raise IndexError('Not support minus index number.')
        node = self._head
        for _ in range(item):
            node = node._next
            if node is None:
                raise IndexError('Invalid index.')
        return node._val

    def __len__(self):
        return self._size

    def push(self, val):
        self._head = SinglyLinkedNode(val, self._head)
        self._size += 1

    def pop(self):
        if self._head is None:
            raise ValueError('No node in list.')
        item = self._head
        self._head = self._head._next
        self._size -= 1
        return item

    def top(self):
        return self._head


def node_numbers(node):
    return 0 if node is None else 1 + node_numbers(node._next)


if __name__ == '__main__':
    sll = SinglyLinkedList()
    for n in range(10):
        sll.push(n)
    print(node_numbers(sll._head))
