from sys import getsizeof

times = 100
array = [None for _ in range(times)]
for _ in range(times):
    print(f"Element numbers: {len(array):<4}, array size: {getsizeof(array)}")
    del array[-1]
print(f"Element numbers: {len(array):<4}, array size: {getsizeof(array)}")