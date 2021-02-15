from ch13.trie.secondary_search_table import Dictionary
from ch13.for_HuffmanCode.heap_remade import Heap


class Trie:
    class _Node:
        __slots__ = 'children', 'index'

        def __init__(self, children=None):
            self.children = children
            self.index = []

        def __repr__(self):
            return f"{self.children}, {self.index}"

    def __init__(self, paragraph=None, children_type=Dictionary, parse_all=False):
        self.children_type = children_type
        self.root = self._Node(self.children_type())
        self.parse_all = parse_all
        if paragraph:
            self._build(paragraph)

    def __repr__(self):
        return f"Trie({', '.join(word for word, _ in self._word_in_trie(self.root))})"

    def _search(self, word):
        node = self.root
        for i, c in enumerate(word):
            child = node.children.get(c)
            if child is None:
                return node, word[i:]
            node = child
        return node, node.index

    def _add_word(self, index, word):
        node, result = self._search(word)
        if isinstance(result, str):
            for c in result:
                new_node = self._Node(self.children_type())
                node.children.add(c, new_node)
                node = new_node
        node.index.append(index)

    @staticmethod
    def _parse(paragraph):
        start = end = 0
        while end < len(paragraph):
            if not paragraph[end].isalpha():
                if start < end:
                    yield start, paragraph[start:end]
                    start = end
                yield start, paragraph[start:end+1]
                start += 1
            end += 1
        if start < end:
            yield start, paragraph[start:end]

    # def _parse(self, paragraph):
    #     word = ''
    #     index = None
    #     for i, char in enumerate(paragraph):
    #         if char.isalpha():
    #             if word == '':
    #                 index = i
    #             word += char
    #         else:
    #             if word:
    #                 yield index, word
    #                 word = ''

    def _build(self, paragraph):
        for i, word in self._parse(paragraph):
            self._add_word(i, word)

    def _word_in_trie(self, node, word=''):
        if node.index:
            yield word, node.index
        if node.children:
            for c, node in node.children.items():
                new_word = word + c
                yield from self._word_in_trie(node, new_word)

    def _yield_all(self, node, level=0):
        for char, node in node.children.items():
            yield level, char, node
            yield from self._yield_all(node, level+1)

    def show_trie(self):
        end = False
        for level, char, node in self._yield_all(self.root):
            if end:
                print(' ' * level, end='', sep='')
                end = False
            print(char, sep='', end='')
            if node.index:
                print('', node.index)
                end = True

    def reconstruction(self):
        heap = Heap()
        for word, indices in self._word_in_trie(self.root):
            for index in indices:
                heap[index] = word
        return ''.join(heap.pop_min() for _ in range(len(heap)))


if __name__ == '__main__':
    # p = "see a bear? sell stock! see a bull? buy stock! bid stock! bid stock! hear the bell? stop!"
    p = 'the thesis is all about thieves.'
    t = Trie(p)
    print(t)
    t.show_trie()
    print(t.reconstruction())
