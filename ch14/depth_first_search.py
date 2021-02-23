from ch14.graphADT_AdjMap import BaseGraphAdjMap


def dfs_tree(graph, vertex, dict_search, out=True):
    for next_vertex, edge in graph.incident_edges(vertex, out):
        if next_vertex not in dict_search:
            dict_search[next_vertex] = edge
            dfs_tree(graph, next_vertex, dict_search, out)


def dfs_forest(graph):
    forest = {}
    for vertex in graph.vertices():
        if vertex not in forest:
            forest[vertex] = None
            dfs_tree(graph, vertex, forest)
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

    forest = dfs_forest(g)
    print(forest)

    roots = [v for v, value in forest.items() if value is None]
    print(roots)
    trees = [{}, {}]
    for i, root in enumerate(roots):
        trees[i][roots[i]] = None
        dfs_tree(g, roots[i], trees[i])
    print(trees)
