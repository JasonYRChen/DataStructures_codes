from ch14.graphADT_AdjMap import BaseGraphAdjMap


def floyd_warshall(graph):
    graph = graph.copy()

    for mid in graph.vertices():
        for start in graph.vertices():
            if start != mid:
                for end in graph.vertices():
                    valid_vertex = end != mid and end != start
                    valid_edge = graph.get_edge(start, mid) and graph.get_edge(mid, end)
                    if valid_vertex and valid_edge:
                        graph.insert_edge(start, end, True, f"{start.element}-{end.element}")
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
    new_g = floyd_warshall(g)
    print(new_g)
    print(new_g.edge_dict)
    print(new_g.vertex_dict[vs['a']])
