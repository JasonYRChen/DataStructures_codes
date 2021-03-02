from ch14.graphADT_AdjMap import BaseGraphAdjMap


def topological_sort_core(graph, found):
    """
    :param graph:
    :param found: dict, {vertex: found sequence}
    :return: None
    """

    for vertex in graph.vertices():
        if vertex not in found:
            ascendant = {v for v in graph.vertex_dict[vertex][False].keys()}
            if ascendant <= found.keys():
                found[vertex] = len(found)
                topological_sort_core(graph, found)
        if len(found) == len(graph.vertex_dict):
            break


def topological_sort_single(graph):
    """ return one of possibilities of topological sort """
    found = {}
    topological_sort_core(graph, found)
    sequence = [None] * len(found)
    for vertex, i in found.items():
        sequence[i] = vertex
    return sequence


def topological_sort_yield(graph, found):
    """
        :param graph:
        :param found: dict, {vertex: found sequence}
        :yield: topological sort combination
        """

    for vertex in graph.vertices():
        if vertex not in found:
            ascendant = {v for v in graph.vertex_dict[vertex][False].keys()}
            if ascendant <= found.keys():
                found[vertex] = len(found)
                if len(found) == len(graph.vertex_dict):
                    yield found
                else:
                    yield from topological_sort_yield(graph, found)
                del found[vertex]


def topological_sort_all(graph):
    """ return all topological sort possibilities"""
    result = []
    for found in topological_sort_yield(graph, {}):
        sequence = [None] * len(found)
        for vertex, i in found.items():
            sequence[i] = vertex
        result.append(sequence)
    return result


def topological_sort_count(graph, found, count):
    """

    :param graph:
    :param found: dict, {vertex: found sequence}
    :param count: list, [int]
    :return:
    """
    for vertex in graph.vertices():
        if vertex not in found:
            ascendant = {v for v in graph.vertex_dict[vertex][False].keys()}
            if ascendant <= found.keys():
                found[vertex] = len(found)
                if len(found) == len(graph.vertex_dict):
                    count[0] += 1
                else:
                    topological_sort_count(graph, found, count)
                del found[vertex]
    return count[0]


if __name__ == '__main__':
    from string import ascii_letters as al

    g = BaseGraphAdjMap()
    g.insert_vertex('a')
    g.insert_vertex('d')
    g.insert_vertex('g')
    g.insert_vertex('b')
    g.insert_vertex('e')
    g.insert_vertex('h')
    g.insert_vertex('c')
    g.insert_vertex('f')
    vs = [v for v in g.vertices()]
    vs.sort(key=lambda x: x.element[-1])
    g.insert_edge(vs[0], vs[2], True, 'a-c')
    g.insert_edge(vs[0], vs[3], True, 'a-d')
    g.insert_edge(vs[2], vs[6], True, 'c-g')
    g.insert_edge(vs[1], vs[0], True, 'b-a')
    g.insert_edge(vs[1], vs[2], True, 'b-c')
    g.insert_edge(vs[3], vs[4], True, 'd-e')
    g.insert_edge(vs[2], vs[4], True, 'c-e')
    g.insert_edge(vs[4], vs[7], True, 'e-h')
    g.insert_edge(vs[5], vs[6], True, 'f-g')
    g.insert_edge(vs[5], vs[2], True, 'f-c')
    g.insert_edge(vs[6], vs[7], True, 'g-h')
    g.insert_edge(vs[0], vs[7], True, 'a-h')
    print(g)
    print()
    topo = topological_sort_single(g)
    print(topo)
    print()
    for comb in topological_sort_all(g):
        print(comb)
    print(topological_sort_count(g, {}, [0]))
