class BaseGraphAdjMap:
    class _Vertex:
        __slots__ = 'element'

        def __init__(self, element=None):
            self.element = element

        def __repr__(self):
            return f"Vertex({self.element})"

    class _Edge:
        __slots__ = 'element', 'vertices', 'directed'

        def __init__(self, element=None, vertices=None, directed=False):
            self.element = element
            self.vertices = vertices
            self.directed = directed

        def endpoints(self):
            return self.vertices

        def opposite(self, vertex):
            if vertex not in self.vertices:
                raise ValueError(f"{self} does not have vertex '{vertex}'")
            return self.vertices[0] if vertex != self.vertices[0] else self.vertices[1]

        def __repr__(self):
            return f"Edge(e={self.element}, directed={self.directed})"

    def __init__(self):
        """
        vertex_dict: {vertex: {
                               True: {for outgoing edge},
                               False: {for incoming edge}
                              }
                     }
        """
        self.edge_dict = {}
        self.vertex_dict = {}

    def __repr__(self):
        return f"{self.__class__.__name__}(edge={self.edge_dict}, vertices={self.vertex_dict})"

    def vertex_count(self):
        return len(self.vertex_dict)

    def vertices(self):
        yield from self.vertex_dict.keys()

    def edge_count(self):
        return len(self.edge_dict)

    def edges(self):
        yield from self.edge_dict.keys()

    def get_edge(self, v_start, v_end):
        edge = self.vertex_dict.get(v_start)
        if edge:
            edge = edge[True].get(v_end)
        return edge

    def degree(self, vertex, out=True):
        return len(self.vertex_dict[vertex][out])

    def incident_edges(self, vertex, out=True):
        yield from self.vertex_dict[vertex][out]

    def insert_vertex(self, element=None):
        vertex = self._Vertex(element)
        self.vertex_dict[vertex] = {True: {}, False: {}}

    def insert_edge(self, start, end, is_directed=False, element=None):
        edge = self._Edge(element, [start, end], is_directed)
        self.edge_dict[edge] = edge
        self.vertex_dict[start][True][end] = edge
        self.vertex_dict[end][False][start] = edge
        if not is_directed:
            self.vertex_dict[start][False][end] = edge
            self.vertex_dict[end][True][start] = edge

    def remove_vertex(self, vertex):
        for edge in list(self.edge_dict.keys()):
            if vertex in edge.vertices:
                self.remove_edge(edge)
        del self.vertex_dict[vertex]

    def remove_edge(self, edge):
        del self.edge_dict[edge]
        [start, end], is_directed = edge.vertices, edge.directed
        del self.vertex_dict[start][True][end]
        del self.vertex_dict[end][False][start]
        if not is_directed:
            del self.vertex_dict[start][False][end]
            del self.vertex_dict[end][True][start]


if __name__ == "__main__":
    from string import ascii_letters as al

    g = BaseGraphAdjMap()
    for c in al[:4]:
        g.insert_vertex(c)
    print(g)
    vs = list(g.vertex_dict.keys())
    g.insert_edge(vs[0], vs[1], True, element='a-b')
    g.insert_edge(vs[0], vs[2], element='a-c')
    g.insert_edge(vs[3], vs[0], True, element='d-a')
    g.insert_edge(vs[1], vs[2], element='b-c')
    print(g)
    print()

    print(vs)
    g.remove_vertex(vs[1])
    vs = list(g.vertex_dict.keys())
    print(vs)
    print(g)

    # es = list(g.edge_dict.keys())
    # print(es)
    # g.remove_edge(es[1])
    # es = list(g.edge_dict.keys())
    # print(es)
    # print(g)

    # node = BaseGraphAdjMap._Node()
    # node.append(1)
    # node.append(2)
    # node.append(133)
    # node._show_nodes()
    #
    # print()
    # graph = BaseGraphAdjMap()
    # graph.edges_root = node
    # result = graph._search_node(3, graph.edges_root)
    # print(result)
