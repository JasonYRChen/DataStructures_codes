from ch11.BinarySearchTree.BinarySearchTree import BinarySearchTree
from collections.abc import MutableMapping


class TreeMap_List(BinarySearchTree, MutableMapping):
    def __init__(self, dict_iter=None):
        self._data = []
        self._size = 0
        if dict_iter:
            self._build_map(dict_iter)