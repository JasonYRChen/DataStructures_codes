a = [list(range(5)), list(range(5, 10)), list(range(10, 15))]
print(sum(sum(arr) for arr in a))
print(sum(range(15)))
