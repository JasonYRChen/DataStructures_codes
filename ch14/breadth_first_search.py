from ch14.graphADT_AdjMap import BaseGraphAdjMap
from collections import deque


def bfs_tree(graph, vertex, dict_search, out=True):
    vertices = deque([vertex])
    while vertices:
        vertex = vertices.popleft()
        for v_oppo, edge in graph.incident_edges(vertex, out):
            if v_oppo not in dict_search:
                dict_search[v_oppo] = edge
                vertices.append(v_oppo)


def bfs_tree2(graph, vertex, dict_search, out=True):
    vertices = [vertex]
    while vertices:
        next_vertices = []
        for v in vertices:
            for v_oppo, edge in graph.incident_edges(v, out):
                if v_oppo not in dict_search:
                    dict_search[v_oppo] = edge
                    next_vertices.append(v_oppo)
        vertices = next_vertices


def bfs_forest(graph):
    vertices = graph.vertices()
    forest = {}
    for vertex in vertices:
        if vertex not in forest:
            forest[vertex] = None
            bfs_tree(graph, vertex, forest)
    return forest


if __name__ == '__main__':
    from string import ascii_letters as al

    g = BaseGraphAdjMap()
    for c in al[:8]:
        g.insert_vertex(c)

    vs = {v.element: v for v in g.vertex_dict.keys()}

    g.insert_edge(vs['a'], vs['b'], element='a-b')
    g.insert_edge(vs['a'], vs['c'], element='a-c')
    g.insert_edge(vs['b'], vs['d'], element='b-d')
    g.insert_edge(vs['c'], vs['d'], element='c-d')
    g.insert_edge(vs['c'], vs['e'], element='c-e')
    g.insert_edge(vs['d'], vs['e'], element='d-e')
    g.insert_edge(vs['f'], vs['g'], element='f-g')
    g.insert_edge(vs['f'], vs['h'], element='f-h')
    g.insert_edge(vs['g'], vs['h'], element='g-h')
    print(g)
    print()
    forest = bfs_forest(g)
    print(forest)
