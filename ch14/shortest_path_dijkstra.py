from ch13.for_HuffmanCode.heap_remade import Heap
from ch14.graphADT_AdjMap import BaseGraphAdjMap
from math import inf


def dijkstra_method(graph, start):
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


if __name__ == '__main__':
    g = BaseGraphAdjMap()
    g.insert_vertex('BOS')
    g.insert_vertex('JFK')
    g.insert_vertex('ORD')
    g.insert_vertex('MIA')
    g.insert_vertex('DFW')
    g.insert_vertex('LAX')
    g.insert_vertex('SFO')
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
    print(g)
    distances = dijkstra_method(g, vs['JFK'])
    print(distances)
