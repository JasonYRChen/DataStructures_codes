class MultaryChildren:
    __slots__ = '_elements', '_parent', '_children'

    def __init__(self, elements=None, parent=None, children=None):
        self._elements = elements
        self._parent = parent
        self._children = children


class BinaryChildren:
    __slots__ = '_elements', '_parent', '_left', '_right'

    def __init__(self, element=None, parent=None, left=None, right=None):
        self._elements = element
        self._parent = parent
        self._left = left
        self._right = right
