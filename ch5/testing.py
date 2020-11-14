a = list(range(5))
print(id(a))
b = list(range(5))
a[:] = b
print(id(a))