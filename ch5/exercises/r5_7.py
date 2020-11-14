from random import shuffle, randint
from collections import defaultdict

n = 10
repeated = randint(1, n)
array = list(range(1, n+1))
array.append(repeated)
shuffle(array)
print(f"Original array: {array}\n")

# Only list is allowed:
result = [0] * (n + 1)
for num in array:
    result[num] += 1
    if result[num] == 2:
        print(f"{num} is repeated")
        break

# defaultdict is allowed
dd = defaultdict(int)
for num in array:
    dd[num] += 1
    if dd[num] == 2:
        print(f"{num} is repeated")
        break
