from collections.abc import Sequence


class DoublyLinkedNode:
    __slots__ = '_val', '_prev', '_next'

    def __init__(self, val=None, prev_node=None, next_node=None):
        self._val = val
        self._prev = prev_node
        self._next = next_node

    def __repr__(self):
        return f"{self.__class__.__name__}(val={self._val}, prev={self._prev._val}, next={self._next._val})"


class Deque:
    def __init__(self, iters=None):
        self._head = DoublyLinkedNode('dummy_head')  # _val to be deleted
        self._tail = DoublyLinkedNode('dummy_tail')  # _val to be deleted
        self._head._prev, self._head._next = self._tail, self._tail
        self._tail._prev, self._tail._next = self._head, self._head
        self._size = 0
        if iters:
            first, last = self._build_nodes(iters)
            self._head._next, first._prev = first, self._head
            self._tail._prev, last._next = last, self._tail

    def __repr__(self):
        """Test no node, 1 node, and 2 or more nodes repr"""
        node, items = self._head._next, []
        for _ in range(len(self)):
            items.append(node._val)
            node = node._next
        return f"{self.__class__.__name__}({items})"

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        new_idx = self._valid_index(index)
        if isinstance(index, slice):
            result = []
            step = 1 if index.step is None else index.step
            curr_idx = 0 if step > 0 else len(self) - 1
            n_p = '_next' if step > 0 else '_prev'
            h_t = '_head' if step > 0 else '_tail'
            node = getattr(getattr(self, h_t), n_p)
            for index in new_idx:
                while curr_idx != index:
                    curr_idx = curr_idx+1 if step > 0 else curr_idx - 1
                    node = getattr(node, n_p)
                result.append(node._val)
            return result

        node = self._head._next
        for _ in range(new_idx):
            node = node._next
        return node._val

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

    def _build_nodes(self, iters):
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
        return first, prev

    def _slice_decompose(self, _slice):
        start, stop, step = _slice.start, _slice.stop, _slice.step
        l_bound, u_bound = 0, len(self) - 1
        if step is None:
            step = 1
        elif step == 0:
            raise ValueError('Slice step cannot be zero.')
        if start is None:
            start = 0 if step > 0 else len(self) - 1
        elif start < 0:
            start += len(self)
        if stop is None:
            stop = len(self) if step > 0 else -1
        elif stop < 0:
            stop += len(self)
        is_interval = abs(stop - (start + step // abs(step))) < abs(stop - start)  # if start +/- 1 step is moving toward stop, then this is an effective interval
        is_overlap = not((start > u_bound and stop >= u_bound) or (start < l_bound and stop <= l_bound))  # check if overlap to (0, len(self))
        if is_interval and is_overlap:
            if start < l_bound:
                start = l_bound
            elif start > u_bound:
                start = u_bound
            if stop < l_bound - 1:
                stop = l_bound - 1
            elif stop > u_bound + 1:
                stop = u_bound + 1
            return start, stop, step
        else:
            return 0, 0, 1

    def _valid_index(self, index):
        if isinstance(index, slice):
            start, stop, step = self._slice_decompose(index)
            return (num for num in range(start, stop, step))

        if not isinstance(index, int):
            raise ValueError('Invalid index. Index should be an integer or a slice.')

        if index < 0:
            index += len(self)
        if (len(self) > 0 and not 0 <= index < len(self)) or (len(self) == 0 and index != 0):
            raise IndexError('Invalid index.')
        return index

    def _list_all(self):
        node = self._head._next
        for _ in range(len(self)):
            print(node)
            node = node._next


if __name__ == '__main__':
    d = Deque(range(6))
    d._list_all()
    print(d[9:-10:-2])