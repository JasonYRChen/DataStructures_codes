from ch14.graphADT_AdjMap import BaseGraphAdjMap
from ch13.for_HuffmanCode.heap_remade import Heap


def prim_jarnik_method(graph):
    """
    This method is not exactly the same code as in the textbook, but the idea is the same.
    """
    vertices = {v for v in graph.vertices()}
    heap = Heap(((e.element, e) for _, e in graph.incident_edges(vertices.pop(), False)))
    shortest_edges = set()

    while vertices and heap:
        _, edge = heap.pop_min()
        v1, v2 = edge.endpoints()
        if (v1 not in vertices) ^ (v2 not in vertices):
            shortest_edges.add(edge)
            vertex = v1 if v1 in vertices else v2
            vertices.remove(vertex)
            for v_oppo, edge in graph.incident_edges(vertex, False):
                if v_oppo in vertices:
                    heap[edge.element] = edge
    return shortest_edges


def kruskal_method(graph):
    """
    This method is not the same code as in the textbook, but the idea is the same.
    """
    clusters = {v: {v} for v in graph.vertices()}
    heap = Heap(((e.element, e) for e in graph.edges()))
    shortest_edges = set()

    while (len(shortest_edges) < graph.vertex_count()-1) and heap:
        _, edge = heap.pop_min()
        v1, v2 = edge.endpoints()
        c_v1, c_v2 = clusters[v1], clusters[v2]
        if c_v1 != c_v2:
            shortest_edges.add(edge)
            # The rests merge two clusters and assign the merged one to each vertex inside
            c_big, c_small = (c_v1, c_v2) if len(c_v1) > len(c_v2) else (c_v2, c_v1)
            c_big.update(c_small)
            for v in c_small:
                clusters[v] = c_big
    return shortest_edges


def min_spanning_tree(shortest_edges, tree_class=BaseGraphAdjMap):
    tree = tree_class()
    vertices = {}
    for edge in shortest_edges:
        v1, v2 = edge.endpoints()
        v1_element, v2_element = v1.element, v2.element
        if v1_element not in vertices:
            v1 = tree.insert_vertex(v1_element)
            vertices[v1_element] = v1
        if v2_element not in vertices:
            v2 = tree.insert_vertex(v2_element)
            vertices[v2_element] = v2
        tree.insert_edge(vertices[v1_element], vertices[v2_element], False, edge.element)
    return tree


if __name__ == '__main__':
    g = BaseGraphAdjMap()
    g.insert_vertex('BOS')
    g.insert_vertex('JFK')
    g.insert_vertex('ORD')
    g.insert_vertex('MIA')
    g.insert_vertex('DFW')
    g.insert_vertex('LAX')
    g.insert_vertex('SFO')
    g.insert_vertex('PVD')
    g.insert_vertex('BWI')
    vs = {v.element: v for v in g.vertices()}
    g.insert_edge(vs['BOS'], vs['SFO'], False, 2704)
    g.insert_edge(vs['BOS'], vs['ORD'], False, 867)
    g.insert_edge(vs['BOS'], vs['JFK'], False, 187)
    g.insert_edge(vs['BOS'], vs['MIA'], False, 1258)
    g.insert_edge(vs['JFK'], vs['ORD'], False, 740)
    g.insert_edge(vs['JFK'], vs['MIA'], False, 1090)
    g.insert_edge(vs['ORD'], vs['SFO'], False, 1846)
    g.insert_edge(vs['ORD'], vs['DFW'], False, 802)
    g.insert_edge(vs['MIA'], vs['DFW'], False, 1121)
    g.insert_edge(vs['MIA'], vs['LAX'], False, 2342)
    g.insert_edge(vs['DFW'], vs['SFO'], False, 1464)
    g.insert_edge(vs['DFW'], vs['LAX'], False, 1235)
    g.insert_edge(vs['SFO'], vs['LAX'], False, 337)
    g.insert_edge(vs['PVD'], vs['ORD'], False, 849)
    g.insert_edge(vs['PVD'], vs['JFK'], False, 144)
    g.insert_edge(vs['BWI'], vs['JFK'], False, 184)
    g.insert_edge(vs['BWI'], vs['MIA'], False, 946)
    g.insert_edge(vs['BWI'], vs['ORD'], False, 621)
    # print(g)
    g2 = prim_jarnik_method(g)
    g3 = kruskal_method(g)
    print(g2)
    print(g3)
    print(g2 == g3)
    print(min_spanning_tree(g2))
    print(min_spanning_tree(g3))
