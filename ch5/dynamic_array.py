from sys import getsizeof
from math import ceil, log2


class Array:
    def __init__(self, *args):
        self.num_element = len(args)
        self.array_size = self._new_array_size(self.num_element)
        self._array = [None for _ in range(self.array_size)]
        self._array[:self.num_element] = args

    def __repr__(self):
        return f"{self._array[:self.num_element]}"

    def __len__(self):
        return self.num_element

    def __getitem__(self, item):
        if 0 <= item < self.num_element:
            return self._array[item]
        elif item <= -1:
            return self._array[self.num_element+item]
        else:
            raise IndexError('Invalid index')

    def append(self, item):
        if self.array_size == self.num_element:
            self.array_size = self._new_array_size(self.num_element+1)
            new_array = [None for _ in range(self.array_size)]
            self._array, new_array[:self.num_element] = new_array, self._array
        self._array[self.num_element] = item
        self.num_element += 1

    @staticmethod
    def _new_array_size(num_element):
        return 2 ** ceil(log2(num_element))


a = Array(1, 2, 3, 4, 5)
print(f"array id: {id(a._array)}, array_size: {a.array_size}, element numbers: {len(a)}, size of array: {getsizeof(a._array)}")
print(f"repr. array: {a}")
print(f"real array: {a._array}", end='\n\n')
for n in range(100, 105):
    a.append(n)
    print(f"array id: {id(a._array)}, array_size: {a.array_size}, element numbers: {len(a)}, size of array: {getsizeof(a._array)}")
    print(f"repr. array: {a}")
    print(f"real array: {a._array}", end='\n\n')
