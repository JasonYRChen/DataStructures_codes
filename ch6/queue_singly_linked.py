class SinglyLinkedNode:
    __slots__ = '_val', '_next'

    def __init__(self, val=0, next_node=None):
        self._val = val
        self._next = next_node

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._val}, next={self._next._val if self._next else None})"


class Queue:
    def __init__(self, seq=None):
        self._head = None
        self._tail = None
        self._size = 0
        if seq:
            node = SinglyLinkedNode()
            for i, s in enumerate(seq):
                node._val = s
                if i == 0:
                    self._head = node
                if i < len(seq) - 1:
                    node._next = SinglyLinkedNode()
                else:
                    self._tail = node
                    self._tail._next = self._head
                node = node._next
                self._size += 1

    def __repr__(self):
        return f"{self.__class__.__name__}(head={self._head}, tail={self._tail}, size={self._size})"

    def __len__(self):
        return self._size

    def __getitem__(self, item):
        if item < 0:
            item += len(self)
        if not 0 <= item < self._size:
            raise IndexError('Invalid index.')
        node = self._head
        for _ in range(item):
            node = node._next
        return node

    def enqueue(self, element):
        if self._head is None:
            self._head = self._tail = SinglyLinkedNode(element)
            self._head._next, self._tail._next = self._tail, self._head
        else:
            self._tail._next = SinglyLinkedNode(element)
            self._tail = self._tail._next
            self._tail._next = self._head
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise AttributeError('Empty queue.')

        item = self._head
        if self._size == 1:
            self._head = self._tail = None
        else:
            self._head = self._head._next
            self._tail._next = self._head
        self._size -= 1
        return item

    def rotate(self, shift):
        if shift < 0:
            raise ValueError('Invalid shift number. Shift number should be larger than or equal to zero.')
        if self._size == 0:
            return self

        for _ in range(shift):
            self._head, self._tail = self._head._next, self._tail._next
        return str(self)

    def insert(self, index, new_node):
        if not isinstance(new_node, SinglyLinkedNode):
            raise ValueError('Invalid node. Please check new node is one of SinglyLinkedNode.')
        if index < 0:
            index += len(self)
        if not 0 <= index < self._size:
            raise IndexError('Invalid index.')
        if index == 0:
            self._head, self._tail._next, new_node._next = new_node, new_node, self._head
        else:
            node = self._head
            for _ in range(index - 1):
                node = node._next
            node._next, new_node._next = new_node, node._next
        self._size += 1

    def remove(self, index):
        if index < 0:
            index += len(self)
        if not 0 <= index < self._size:
            raise IndexError('Invalid index.')

        if self._size == 1:
            self._head = self._tail = None
        else:
            if index == 0:
                self._head, self._tail._next = self._head._next, self._head._next
            else:
                node = self._head
                for _ in range(index):
                    prev, node = node, node._next
                prev._next = node._next
        self._size -= 1

    def list_all(self):
        node = self._head
        for _ in range(self._size):
            print(node)
            node = node._next


if __name__ == "__main__":
    q = Queue(range(10))
    q.insert(3, SinglyLinkedNode(100))
    # q.list_all()

    node = q._head._next
    numbers = 1
    while id(node) != id(q._head):
        numbers += 1
        node = node._next
    print(numbers)

