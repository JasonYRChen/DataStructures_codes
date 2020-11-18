from math import ceil, log2


class Dequeue:
    def __init__(self, iterables=None):
        self._head = 0
        self._end = 0
        self._array = self._make_array(iterables, initial=True)

    def __len__(self):
        head, end = self._head, self._end
        if self._array[head] is None:
            return 0
        return end - head + 1 if end >= head else len(self._array) - head + end + 1

    def __getitem__(self, item):
        if isinstance(item, slice):
            head, end = self._head, self._end
            array = self._array[head:end + 1] if end >= head else self._array[head:] + self._array[:end + 1]
            return Dequeue(array[item])

        if 0 <= item < len(self):
            return self._array[(self._head + item) % len(self._array)]
        elif -1 >= item >= -len(self):
            return self._array[(self._head + (item % len(self))) % len(self._array)]
        else:
            raise IndexError('Invalid index.')

    def __repr__(self):
        head, end = self._head, self._end
        if self._array[head] is None:
            return f"{self.__class__.__name__}([])"
        array = self._array[head:end+1] if end >= head else self._array[head:] + self._array[:end+1]
        return f"{self.__class__.__name__}({array})"

    def _full_array(self):
        return f"{self.__class__.__name__}({self._array})"

    def _make_array(self, prev_array, initial=False):
        if prev_array is None:
            return [None, None]

        head, end = (0, len(prev_array)-1) if initial else (self._head, self._end)
        length = end - head + 1 if end >= head else len(self._array) - head + end + 1
        new_length = 2 ** (ceil(log2(length)) + 1)
        new_array = [None] * new_length
        if head <= end:
            new_array[1:length+1] = prev_array[head:end+1]
        else:
            first_section = len(prev_array)-head
            new_array[1:first_section+1] = prev_array[head:]
            new_array[first_section+1:first_section+end+2] = prev_array[:end+1]
        self._head, self._end = 1, length
        return new_array

    def append(self, element):
        array, end = self._array, self._end
        if array[end] is None:
            array[end] = element
            return

        if array[(end + 1) % len(array)] is not None:
            self._array = self._make_array(array)
        array, next_end = self._array, (self._end + 1) % len(self._array)
        array[next_end] = element
        self._end = next_end

    def appendleft(self, element):
        array, head = self._array, self._head
        if array[head] is None:
            array[head] = element
            return

        if array[(head - 1) % len(array)] is not None:
            self._array = self._make_array(array)
        array, next_head = self._array, (self._head - 1) % len(self._array)
        array[next_head] = element
        self._head = next_head

    def insert(self, idx, element):
        if idx < 0:
            idx = len(self) + idx
        if not 0 <= idx < len(self):
            raise IndexError('Invalid index.')

        next_end = (self._end + 1) % len(self._array)
        if self._array[next_end] is not None:
            self._array = self._make_array(self._array)

        array = self._array
        idx = (idx + self._head) % len(array)
        end = self._end if self._end >= self._head else self._head + len(self) - 1
        for i in range(end, idx-1, -1):
            prev, curr = (i+1) % len(array), i % len(array)
            array[prev] = array[curr]
        array[idx] = element
        self._end = (self._end + 1) % len(array)

    def remove(self, idx):
        if idx < 0:
            idx = len(self) + idx
        if not 0 <= idx < len(self):
            raise IndexError('Invalid index.')

        array = self._array
        idx = (self._head + idx) % len(array)
        end = self._end if self._end >= self._head else self._head + len(self) - 1
        for i in range(idx, end):
            i, i_next = i % len(array), (i+1) % len(array)
            array[i] = array[i_next]
        array[end] = None
        self._end = (end - 1) % len(array)
        self._shrink()

    def _shrink(self):
        """shrink self._array if real size is half smaller than len(self._array) and rearrange array"""
        if len(self) <= len(self._array) // 4:
            self._array = self._make_array(self._array)

    def pop(self):
        head, end, array = self._head, self._end, self._array
        if array[head] is None:
            raise ValueError('Empty dequeue.')
        item = array[end]
        array[end] = None
        self._end = (end - 1) % len(array)
        if array[head] is None:
            self._head = self._end = 1
        self._shrink()
        return item

    def popleft(self):
        head, end, array = self._head, self._end, self._array
        if array[end] is None:
            raise ValueError('Empty dequeue.')
        item = array[head]
        array[head] = None
        self._head = (head + 1) % len(array)
        if array[end] is None:
            self._head = self._end = 1
        self._shrink()
        return item


if __name__ == '__main__':
    a = list(range(4))
    a = Dequeue(a)
    print(a, ', length:', len(a))
    print(a._full_array(), end='\n\n')
    a._array[5:] = [5, 6, 7]
    a._array[0] = 11
    a._array[1] = None
    a._head, a._end = 2, 0
    print(a)
    print(a._full_array(), end='\n\n')
    a._array = a._make_array(a._array)
    print(a)
    print(a._full_array(), end='\n\n')
    a._end = 2
    a._array = a._make_array(a._array)
    print(a)
    print(a._full_array(), end='\n\n')
    a.insert(-1, 33)
    a.insert(-1, 44)
    a.insert(-1, 55)
    a.insert(1, 66)
    a.insert(0, 77)
    a.insert(0, 88)
    a.insert(-1, 99)
    print(a)
    print(a._full_array(), end='\n\n')
    a.remove(-1)
    a.remove(-3)
    a.remove(0)
    a.remove(3)
    a.remove(3)
    a.remove(3)
    a.remove(0)
    print(a)
    print(a._full_array(), end='\n\n')
    a.append(100)
    a.append(200)
    a.append(300)
    a.appendleft(-100)
    a.appendleft(-200)
    a.appendleft(-300)
    print(a)
    print(a._full_array(), end='\n\n')
    print('pop:', a.pop())
    print('pop:', a.pop())
    print('pop:', a.pop())
    print('pop:', a.pop())
    print('pop:', a.pop())
    print('pop:', a.pop())
    print('pop:', a.popleft())
    print('pop:', a.pop())
    print('pop:', a.pop())
    print(a)
    print(a._full_array(), end='\n\n')
