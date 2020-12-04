t = ['n', 1]

def a():
    if t[0] is not None:
        yield t[0]
    if t[1] is not None:
        yield t[1]


print(next(a()))