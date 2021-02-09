class Heap:
    class _Node:
        __slots__ = 'key', 'value'

        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value

        def __repr__(self):
            return f"{self.key}={self.value}"

        def __lt__(self, other):
            return self.key < other

        def __gt__(self, other):
            return self.key > other

    def __init__(self, items=None):
        self.data = []
        if items:
            for k, v in items:
                self[k] = v

    def __repr__(self):
        return f"Heap({', '.join(str(node) for node in self.data)})"

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        self.data.append(self._Node(key, value))
        self._upward(len(self) - 1)

    def _upward(self, index):
        parent = self.parent(index)
        while parent >= 0 and self.data[parent] > self.data[index]:
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index, parent = parent, self.parent(parent)

    def _downward(self, index):
        while True:
            l_idx, r_idx = self.left(index), self.right(index)
            left = self.data[l_idx] if l_idx < len(self) else None
            right = self.data[r_idx] if r_idx < len(self) else None
            current = self.data[index]
            if left and left < current and ((right and left < right) or not right):
                self.data[l_idx], self.data[index] = self.data[index], self.data[l_idx]
                index = l_idx
            elif right and right < current:
                self.data[r_idx], self.data[index] = self.data[index], self.data[r_idx]
                index = r_idx
            else:
                break

    @staticmethod
    def left(index):
        return 2 * index + 1

    @staticmethod
    def right(index):
        return 2 * index + 2

    @staticmethod
    def parent(index):
        return (index - 1) // 2

    def min(self):
        if self.data[0]:
            return self.data[0].value
        raise ValueError('Empty heap.')

    def pop_min(self):
        if not self.data:
            raise ValueError('Empty heap.')
        value = self.data[0].value
        last = self.data.pop()
        if len(self) > 0:
            self.data[0] = last
            self._downward(0)
        return value


if __name__ == '__main__':
    a = [(9, 9), (7, 7), (1, 1), (2, 2), (1, 1), (3, 3), (0, 0), (6, 6), (10, 10), (4, 4), (5, 5)]
    h = Heap(a)
    print(h)
    for _ in range(11):
        print(h.pop_min())
    print(h)
