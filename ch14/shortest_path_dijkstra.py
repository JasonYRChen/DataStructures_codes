from ch13.for_HuffmanCode.heap_remade import Heap
from ch14.graphADT_AdjMap import BaseGraphAdjMap
from math import inf


def dijkstra_method(graph, start):
    """ This function can detect if start vertex can reach to any vertices in the
        rest of the graph. If any vertex cannot be reached, then
        distances[vertex cannot be reached] = inf.
    """
    heap = Heap([(0, start)])
    found = set()
    distances = {v: inf for v in graph.vertices()}
    distances[start] = 0
    while heap and len(found) < graph.vertex_count():
        distance, vertex = heap.pop_min()
        if vertex not in found:
            found.add(vertex)
            distances[vertex] = distance
            for v_oppo, edge in graph.incident_edges(vertex):
                if v_oppo not in found:
                    heap[edge.element+distances[vertex]] = v_oppo
    return distances


def dijkstra_method_simplify(graph, start):
    """ This function cannot report unreachable vertices at the beginning. One
        should compare the distances's key with graph's vertices to show those
        unreachable vertices.
    """
    heap = Heap([(0, start)])
    distances = {}
    while heap and len(distances) < graph.vertex_count():
        distance, vertex = heap.pop_min()
        if vertex not in distances:
            distances[vertex] = distance
            for v_oppo, edge in graph.incident_edges(vertex):
                if v_oppo not in distances:
                    heap[edge.element+distances[vertex]] = v_oppo
    return distances


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
    departure = 'BWI'
    d1 = dijkstra_method(g, vs[departure])
    d2 = dijkstra_method_simplify(g, vs[departure])
    print(d1)
    print(d1 == d2)
