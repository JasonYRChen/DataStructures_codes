from ch8.tree.LinkedBinaryTree.LinkedBinaryTree import LinkedBinaryTree


class Arithmetic(LinkedBinaryTree):
    _op = {'+', '-', '*', '/'}
    _p_n_op = {'+', '-'}
    _parentheses = '(', ')'
    _rest_op = _op - _p_n_op
    _nums = '.0123456789'

    def __init__(self, expr=''):
        super().__init__()
        self.expression = expr

    def __repr__(self):
        p_n_detect = False  # detect if '+' or "-" appear. If so, expression need parenthesis to protect.
        expr = ''
        for _, node in self.postorder():
            e = self.element(node)
            if e in self._p_n_op:
                p_n_detect = True
            elif p_n_detect and e in self._rest_op:
                expr = '(' + expr + ')'
                p_n_detect = False
            expr += str(e)
        return expr

    @property
    def expression(self):
        return self._expr

    @expression.setter
    def expression(self, expr):
        if not isinstance(expr, str):
            raise TypeError('Formula should be string type.')
        self._expr = expr

    def evaluate(self):
        """Do four fundamental arithmetic operations."""
        return self._evaluate(self.root())

    def _evaluate(self, node):
        if self.is_leaf(node):
            return float(self.element(node))
        left = self._evaluate(self.left(node))
        right = self._evaluate(self.right(node))
        op = self.element(node)
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left / right

    def parse(self):
        pass

    def _parse(self, expr: str, nodes: list, cursor: list):
        num = ''
        while cursor[-1] < len(expr):
            c = expr[cursor[-1]]
            if c in self._nums:
                num += c
            elif c in self._op:
                nodes.append(self._make_node(float(num)))
                num = ''
                if len(nodes) > 2 and nodes[-2] in self._rest_op:
                    right = nodes.pop()
                    op = nodes.pop()
                    left = nodes.pop()
                    node = self.attach(op, left, right)
                    nodes.append(node)
                nodes.append(self._make_node(c))
            elif c == '(':
                self._parse(expr, nodes, cursor)
            elif c == ')':
                # do node combination
                return None
            cursor[-1] += 1
        if num:
            nodes.append(self._make_node(float(num)))
        # do node combination and make root

    def _merge_nodes(self, nodes: list):
        top_node = None
        while nodes:
            right = top_node if top_node is not None else nodes.pop()
            op = nodes.pop()
            left = nodes.pop()
            top_node = self.attach(op, left, right)
        return top_node


if __name__ == '__main__':
    a = Arithmetic()
    nodes = [a._Node(3), a._Node('*'), a._Node(1), a._Node('+'), a._Node(2)]
    node = a._merge_nodes(nodes)
    a._add_root(node)
    a.list_all()
    # print(a)
