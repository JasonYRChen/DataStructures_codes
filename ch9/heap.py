from ch9.tree.ArrayBinaryTree import ArrayBinaryTree
from collections.abc import Iterable


class Heap(ArrayBinaryTree):
    def add(self, key, element):
        index = self._num_node
        self._data.append(self._Node(key, element, index))
        self._upheap(index)
        self._num_node += 1

    def _upheap(self, index, key=None):
        parent_idx = self._parent(index)
        func = self.key if key is None else lambda x: key(self.element(x))
        if index and func(index) < func(parent_idx):
            self[parent_idx], self[index] = self[index], self[parent_idx]
            self.set_index(parent_idx, parent_idx)
            self.set_index(index, index)
            self._upheap(parent_idx)

    def _downheap(self, index, key=len):
        if self._num_children(index):
            children = [c for c in self._children(index) if self[c] is not None]
            func = self.key if key is None else lambda x: key(self.element(x))
            child_idx = min(children, key=lambda idx: func(idx))
            if func(index) > func(child_idx):
                self[index], self[child_idx] = self[child_idx], self[index]
                self.set_index(child_idx, child_idx)
                self.set_index(index, index)
                self._downheap(child_idx)

    def remove_min(self):
        if self._is_empty():
            raise ValueError('Empty tree.')
        min_key, min_element = self.key(0), self.element(0)
        self[0] = self[-1]
        del self[-1]
        self._downheap(0)
        self._num_node -= 1
        return min_key, min_element

    def min(self):
        if self._is_empty():
            raise ValueError('Empty tree.')
        return self.key(0), self.element(0)

    def _build_tree(self, iterables):
        if not isinstance(iterables, Iterable):
            raise TypeError('Invalid iterable. Cannot initiate a heap.')
        if len(self):
            raise ValueError('Heap already exist.')
        self._data = [self._Node(k, e, i) for i, (k, e) in enumerate(iterables)]
        self._num_node = len(self._data)
        h = self.height()
        if h:
            start = 2 ** h - 1
            for index in range(start-1, -1, -1):
                self._downheap(index)

    def sort(self, descending=True, key=None):
        pass

    def _sort(self, index, key=None):
        pass


if __name__ == '__main__':
    rank = (2, 'Shawn'), (4, 'Ian'), (1, 'Jason'), (11, 'Bob'), (1, 'Ryan'), (5, 'Chris'), (13, 'Wu'), (8, 'Nick'), (7, 'Rick')
    h = Heap(rank)
    print(h.min())
    print(h)
    print('length:', len(h), 'height:', h.height())
    h.list_all(h.breadth_first)
    # print(h.remove_min())
    # print(h.remove_min())
    # print('length:', len(h), 'height:', h.height())
    # h.list_all(h.breadth_first)
    # print(h.remove_min())
    # print(h.remove_min())
    # print(h.remove_min())
    # print(h.remove_min())
    # print(h.remove_min())
    # print(h.remove_min())
    # print(h.remove_min())
    # print(h)
    # print('length:', len(h))
    # h.list_all()
