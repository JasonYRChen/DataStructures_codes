class Test:
    class _Node:
        pass

    def _test(self, node):
        if not isinstance(node, self._Node):
            print(False)
        print(True)


class _Node:
    pass


t = Test()
u = Test()._Node()
print(t._test(u))