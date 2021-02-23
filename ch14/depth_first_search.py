from ch14.graphADT_AdjMap import BaseGraphAdjMap


def dfs_tree(graph, vertex, dict_search, out=True):
    for edge in graph.incident_edges(vertex, out):
        next_vertex = edge.opposite(vertex)
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
    print(g)

    vs = list(g.vertex_dict.keys())
    vs.sort(key=lambda x: x.element)
    print(vs)
