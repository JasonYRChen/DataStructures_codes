# O(n^2) running time
def inplace_sort(array, descending=True):
    compare = (lambda x, y: x > y) if descending else (lambda x, y: x < y)

    for i in range(1, len(array)):
        for j in range(i-1, -1, -1):
            if compare(array[i], array[j]):
                array[i], array[j], i = array[j], array[i], j
    return array


if __name__ == '__main__':
    from random import randrange

    # Test of insert_sort function
    array = [randrange(-10, 10) for _ in range(5)]
    print('Original array:', array)
    print('Sorted array:  ', inplace_sort(array, False))
