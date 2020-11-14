from sys import getsizeof

times = 1000
array = []
size = getsizeof(array)
for i in range(times):
    if getsizeof(array) != size:
        print(f"Array size: {size:<4}, element numbers: {len(array)-1}")
        size = getsizeof(array)
    array.append(None)
