from ch9.tree.ArrayBinaryTree import ArrayBinaryTree
from collections.abc import Iterable


class HeapQ(ArrayBinaryTree):
    class _HeapNode(ArrayBinaryTree._Node):
        def __lt__(self, other):
            return self._element < other._element

        def __eq__(self, other):
            return self._element == other._element

        def __repr__(self):
            return f"Node(e={self._element}, i={self._index})"

    def __init__(self, elements=None, key=None, ascending=True):
        self._ascending = ascending
        self._key = lambda idx: key(self.element(idx)) if key is not None else lambda idx: self.element(idx)
        self._data = []
        if elements is not None:
            self._build_tree(elements, key, ascending)

    def __len__(self):
        return len(self._data)

    def _build_tree(self, iterables, key=None, ascending=None):
        if iterables is not None and not isinstance(iterables, Iterable):
            raise TypeError('Invalid iterable or sequence.')
        if iterables is not None:
            self._data = [self._HeapNode(element=e, index=i) for i, e in enumerate(iterables)]
        for index in range(len(self)-1, -1, -1):
            self._downheap(index, len(self), key, ascending)

    def _left(self, index, end=None):
        index = self._positive_index(index)
        if end is None:
            end = len(self)
        left_index = 2 * index + 1
        if left_index < end:
            return left_index
        return None

    def _right(self, index, end=None):
        index = self._positive_index(index)
        if end is None:
            end = len(self)
        right_index = 2 * index + 2
        if right_index < end:
            return right_index
        return None

    def _children(self, index, end=None):
        index = self._positive_index(index)
        if self._left(index) is not None:
            yield self._left(index, end)
        if self._right(index) is not None:
            yield self._right(index, end)

    def _num_children(self, index, end=None):
        index = self._positive_index(index)
        return sum(int(n is not None) for n in self._children(index, end))

    def _is_leaf(self, index, end=None):
        index = self._positive_index(index)
        return self._num_children(index, end) == 0

    def _positive_index(self, index):
        if index < 0:
            return len(self) + index
        return index

    def _upheap(self, index, key=None, ascending=None):
        index = self._positive_index(index)
        if index:
            ascending = ascending if ascending is not None else self._ascending
            func = self._key if key is None else lambda idx: key(self.element(idx))
            parent_idx = self._parent(index)
            if not(ascending ^ (func(index) < func(parent_idx))):
                self[index], self[parent_idx] = self[parent_idx], self[index]
                self.set_index(index, index)
                self.set_index(parent_idx, parent_idx)
                self._upheap(parent_idx, key, ascending)

    def _downheap(self, index, end=None, key=None, ascending=None):
        """ Do down heap recursively according to 'key' function

            :param
                index: the current index
                end: the length of effective heap starting from index 0. This is specialized for 'sort' method
                key: a function returning comparable value
                ascending: whether the heap is arranged in ascending way or otherwise
        """
        index = self._positive_index(index)
        if not self._is_leaf(index, end):
            ascending = ascending if ascending is not None else self._ascending
            func = self._key if key is None else lambda idx: key(self.element(idx))
            min_max = min if ascending else max
            child_index = min_max((idx for idx in self._children(index, end) if idx is not None), key=func)
            if ascending ^ (func(index) < func(child_index)):
                self[index], self[child_index] = self[child_index], self[index]
                self.set_index(index, index)
                self.set_index(child_index, child_index)
                self._downheap(child_index, end, key, ascending)

    def push(self, element):
        self._data.append(self._HeapNode(None, element, len(self)))
        self._upheap(-1)

    def remove(self, index):
        if index >= len(self):
            raise IndexError('Invalid index')
        index = self._positive_index(index)
        element = self.element(index)
        self[index] = self._data.pop()
        self._downheap(index)
        return element

    def pop(self):
        if len(self) == 0:
            raise ValueError('Empty heap.')
        if len(self) == 1:
            element = self.element(0)
            self._data.pop()
            return element
        return self.remove(0)

    def pushpop(self, element):
        # Because of self._key need data index as parameter, here I use an indirect
        # implement to compare element and data[0]
        self._data.append(self._HeapNode(None, element, len(self)))
        func = self._key
        if self._ascending ^ (func(-1) >= func(0)):
            print('direct giveback')
            element = self.element(-1)
            self._data.pop()
            return element
        print('push then pop')
        self._data.pop()
        self.push(element)
        return self.pop()

    def min(self):
        if self._ascending:
            return self.element(0)
        return min(self._data)

    def max(self):
        if not self._ascending:
            return self.element(0)
        return max(self._data)

    def update(self, index, element):
        index = self._positive_index(index)
        self.set_element(index, element)
        parent_idx = self._parent(index)
        if parent_idx and (self._ascending ^ (self._key(index) >= self._key(parent_idx))):
            self._upheap(index)
        else:
            self._downheap(index)

    def heapify(self, iterables=None, key=None, ascending=None):
        self._build_tree(iterables, key, ascending)

    def nlargest(self, n):
        original = self._data.copy()
        if self._ascending:
            self.heapify(ascending=False)
        result = [self.pop() for _ in range(n)]

        # recover to original heap, including indices of each element
        self._data = original
        for i in range(len(self)):
            self.set_index(i, i)
        return result

    def nsmallest(self, n):
        original = self._data.copy()
        if not self._ascending:
            self.heapify()
        result = [self.pop() for _ in range(n)]

        # recover to original heap, including indices of each element
        self._data = original
        for i in range(len(self)):
            self.set_index(i, i)
        return result

    def sort(self, key=None, ascending=None):
        if key is not None:
            self._key = key
        if ascending is not None and (ascending != self._ascending):
            self._ascending = ascending
            self.heapify()
        for i in range(len(self)-1, 0, -1):
            self[0], self[i] = self[i], self[0]
            self._downheap(0, i)
        return [self.element(idx) for idx in range(len(self)-1, -1, -1)]


if __name__ == '__main__':
    nums = 4, 3, 7, 8, 1, 0, 11, 34, 2
    h = HeapQ(nums, ascending=False, key=lambda x: x % 10)
    h.list_all(h.breadth_first)
    print(h.pushpop(435))
    print(h)
    print(len(h))
    h.list_all(h.breadth_first)
