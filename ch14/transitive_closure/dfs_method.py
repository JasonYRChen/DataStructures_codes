from ch14.graphADT_AdjMap import BaseGraphAdjMap


def dfs(graph, vertex_base, next_vertex, vertex_found):
    vertex_edge = [(v, e) for v, e in graph.incident_edges(next_vertex)]
    for vertex, _ in vertex_edge:
        if vertex not in vertex_found:
            if not graph.get_edge(vertex_base, vertex):
                graph.insert_edge(vertex_base, vertex, True, f"{vertex_base.element}-{vertex.element}")
            vertex_found.add(vertex)
            dfs(graph, vertex_base, vertex, vertex_found)


def dfs_method(graph):
    graph = graph.copy()

    for vertex in graph.vertices():
        found = {vertex}
        dfs(graph, vertex, vertex, found)
    return graph


if __name__ == '__main__':
    from string import ascii_letters as al

    g = BaseGraphAdjMap()
    for char in al[:7]:
        g.insert_vertex(char)
    vs = {v.element: v for v in g.vertices()}
    g.insert_edge(vs['a'], vs['e'], True, 'a-e')
    g.insert_edge(vs['b'], vs['a'], True, 'b-a')
    g.insert_edge(vs['d'], vs['b'], True, 'd-b')
    g.insert_edge(vs['d'], vs['e'], True, 'd-e')
    g.insert_edge(vs['f'], vs['d'], True, 'f-d')
    g.insert_edge(vs['e'], vs['g'], True, 'e-g')
    g.insert_edge(vs['g'], vs['c'], True, 'g-c')
    g.insert_edge(vs['c'], vs['f'], True, 'c-f')
    print(g)
    new_g = dfs_method(g)
    print(new_g)
    print(new_g.edge_dict)
    print(new_g.vertex_dict[vs['a']])

    complete_set = set()
    for head in al[:7]:
        for end in al[:7]:
            if end != head:
                complete_set.add(head+'-'+end)
    edge_set = {edge.element for edge in new_g.edge_dict.keys()}
    edge_list = [edge.element for edge in new_g.edge_dict.keys()]
    print(edge_set == complete_set)
    print(len(edge_list) == len(edge_set))
