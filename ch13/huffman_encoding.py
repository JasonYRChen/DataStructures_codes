from ch13.for_HuffmanCode.huffman_tree import HuffmanTree
from ch13.for_HuffmanCode.heap_remade import Heap
from collections import defaultdict


class HuffmanCode:
    def __init__(self, string):
        self.tree = None
        if string != '':
            table = self._freq_table(string)
            self._build_tree(table)

    def __repr__(self):
        nodes = list(self._take_all_leaves(self.tree.root))
        return f"{self.__class__.__name__}({', '.join(str(node.value)+': '+str(node.key) for node in nodes)})"

    def encode(self, string):
        pass

    def decode(self, code):
        pass

    def _build_tree(self, freq_table):
        heap = Heap()
        for char, freq in freq_table.items():
            heap[freq] = HuffmanTree(char, freq)

        while len(heap) > 1:
            t1 = heap.pop_min()
            t2 = heap.pop_min()
            t = t2 + t1
            heap[t.key()] = t
        tree = heap.pop_min()
        self.tree = tree

    @staticmethod
    def _freq_table(string):
        table = defaultdict(int)
        for c in string:
            table[c] += 1
        return table

    def _take_all_leaves(self, node):
        if node.left is None and node.right is None:
            yield node
        if node.left:
            yield from self._take_all_leaves(node.left)
        if node.right:
            yield from self._take_all_leaves(node.right)


if __name__ == '__main__':
    s = 'This is a testing string containing many "s".'
    h = HuffmanCode(s)
    print(h)
    h.tree.show_hierarchy()
