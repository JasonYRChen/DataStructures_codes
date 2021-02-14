from ch13.trie.secondary_search_table import Dictionary


class Trie:
    class _Node:
        __slots__ = 'children', 'index'

        def __init__(self, children=None):
            self.children = children
            self.index = []

        def __repr__(self):
            return f"{self.children}, {self.index}"

    def __init__(self, paragraph=None, children_type=Dictionary):
        self.children_type = children_type
        self.root = self._Node(self.children_type())
        if paragraph:
            self._build(paragraph)

    def __repr__(self):
        return f"Trie({', '.join(word for word in self._word_in_trie(self.root))})"

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
        word = ''
        index = None
        for i, char in enumerate(paragraph):
            if char.isalpha():
                if word == '':
                    index = i
                word += char
            else:
                if word:
                    yield index, word
                    word = ''

    def _build(self, paragraph):
        for i, word in self._parse(paragraph):
            self._add_word(i, word)

    def _word_in_trie(self, node, word=''):
        if node.children:
            for c, node in node.children.items():
                new_word = word + c
                yield from self._word_in_trie(node, new_word)
        else:
            yield word


if __name__ == '__main__':
    p = "see a bear? sell stock! see a bull? buy stock! bid stock! bid stock! hear the bell? stop!"
    t = Trie(p)
    print(t)
