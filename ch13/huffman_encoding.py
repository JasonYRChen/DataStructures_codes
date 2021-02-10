from ch13.for_HuffmanCode.huffman_tree import HuffmanTree
from ch13.for_HuffmanCode.heap_remade import Heap
from collections import defaultdict


class HuffmanCode:
    def __init__(self, string=''):
        self.tree = None
        self.encode_dict = None
        if string != '':
            self._build_tree(self._freq_table(string))

    def __repr__(self):
        nodes = list(node for node, _ in self._take_all_leaves(self.tree.root))
        return f"{self.__class__.__name__}({', '.join(str(node.value)+': '+str(node.key) for node in nodes)})"

    def encode(self, string):
        if self.tree is None:
            self._build_tree(self._freq_table(string))
            self._encode_dict()
        if self.encode_dict is None:
            self._encode_dict()

        code = ''
        for char in string:
            code += self.encode_dict[char]
        return code

    def _encode_dict(self):
        encode_dict = {node.value: code for node, code in self._take_all_leaves(self.tree.root)}
        self.encode_dict = encode_dict
        return encode_dict

    def decode(self, code):
        node = self.tree.root
        string = ''
        for bin in code:
            valid_bin = False
            if bin == '0' and node.left:
                node = node.left
            elif bin == '1' and node.right:
                node = node.right
            if node.left is None and node.right is None:
                string += node.value
                node = self.tree.root
                valid_bin = True
        if not valid_bin:
            raise ValueError('Invalid code. Incorrect decoding.')
        return string

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

    def _take_all_leaves(self, node, code=''):
        if node.left is None and node.right is None:
            yield node, code
        if node.left:
            yield from self._take_all_leaves(node.left, code+'0')
        if node.right:
            yield from self._take_all_leaves(node.right, code+'1')


if __name__ == '__main__':
    s = 'This is a testing string containing many "s".'
    c = '11101111000111010000111010001000000110100101101110011010001100010111000101001101000110000010010010000101101000011010011010001100010011100001000101100011111011111100100'

    h = HuffmanCode()
    code = h.encode(s)
    decode_s = h.decode(code)
    print(h)
    print('Original string:', s)
    print('Huffman code:', code)
    print('Decoded string:', decode_s)
