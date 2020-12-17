import math as m
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#import netgraph


class HalfEdge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.twin = None
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"E(o:[{self.origin.x}, {self.origin.y}], d:[{self.destination.x}, {self.destination.y}])"

    def __eq__(self, rhs):
        return self.origin is rhs.origin and self.destination is rhs.destination

    def get_length(self):
        return m.sqrt((self.destination.x - self.origin.x)**2 + (self.destination.y - self.origin.y)**2)

    def get_angle(self):
        dx = self.destination.x - self.origin.x
        dy = self.destination.y - self.origin.y
        l = m.sqrt(dx * dx + dy * dy)
        if dy > 0:
            return m.acos(dx / l)
        else:
            return 2 * m.pi - m.acos(dx / l)


class Vertex:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return f"Vertex coords: ({self.x}, {self.y})"

    def __eq__(self, rhs):
        return self.x is rhs.x and self.y is rhs.y

    def __hash__(self):
        return hash(self.x) + hash(self.y)


class EdgesMap:
    def __init__(self):
        # origin -> destination -> edge
        self.origin_destination_map = {}
        # destination -> origina -> edge
        self.destination_origin_map = {}

    def insert_edge(self, origin, destination, edge):
        self.origin_destination_map.setdefault(origin, {})
        self.origin_destination_map[origin][destination] = edge

        self.destination_origin_map.setdefault(destination, {})
        self.destination_origin_map[destination][origin] = edge

    def get_edge(self, origin, destination):
        return self.origin_destination_map[origin][destination]

    def get_outgoing_edges(self, origin):
        outgoing_edges = list(self.origin_destination_map[origin].values())
        return outgoing_edges

    def get_incoming_edges(self, destination):
        incoming_edges = list(self.destination_origin_map[destination].values())
        return incoming_edges

    # Returns outgoing edges in clockwise order
    def get_outgoing_edges_clockwise(self, origin):
        outgoing_edges = list(self.origin_destination_map[origin].values())
        outgoing_edges.sort(key = lambda edge : edge.get_angle(), reverse=True)
        return outgoing_edges

    # Returns incoming edges in clockwise order
    def get_incoming_edges_clockwise(self, destination):
        incoming_edges = list(self.destination_origin_map[destination].values())
        incoming_edges.sort(key = lambda edge : edge.get_angle(), reverse=True)
        return incoming_edges

    # Returns all the incoming and outgoing edges
    def get_all_edges_of_vertex(self, vertex):
        edges = self.get_incoming_edges_clockwise(vertex) + self.get_outgoing_edges(vertex)
        return edges

    # Deletes edge from the mapping
    def delete_edge(self, origin, destination):
        del self.origin_destination_map[origin][destination]
        del self.destination_origin_map[destination][origin]


class Dcel:
    def __init__(self):
        # (x coordinate, y coordinate) -> vertex
        self.vertices_map = {}
        self.edges_map = EdgesMap()

    def build_dcel(self, points, segments):
        # Creates a hashmap point_coordinates->vertex
        label = 'A'
        for point in points:
            self.vertices_map[point] = Vertex(point[0], point[1], label)
            label = chr(ord(label) + 1)

        # Connects vertices and edges and assign twins
        for segment in segments:
            origin = self.vertices_map[segment[0]]
            destination = self.vertices_map[segment[1]]

            half_edge = HalfEdge(origin, destination)
            twin_half_edge = HalfEdge(destination, origin)

            half_edge.twin = twin_half_edge
            twin_half_edge.twin = half_edge

            self.edges_map.insert_edge(half_edge.origin, half_edge.destination, half_edge)
            self.edges_map.insert_edge(twin_half_edge.origin, twin_half_edge.destination, twin_half_edge)

        # Identify next and previous half edges
        for vertex in list(self.vertices_map.values()):
            outgoing_edges = self.edges_map.get_outgoing_edges_clockwise(vertex)
            print(outgoing_edges)
            # Consider the outgoing edges in clockwise order
            # Assign to the twin of each outgoing edge the next ougoing edge
            for i in range(len(outgoing_edges)):
                h1 = outgoing_edges[i]
                h2 = outgoing_edges[(i+1) % len(outgoing_edges)]
                h1.twin.next = h2
                h2.prev = h1.twin

    def __get_graph_plot__(self):
        Graph = nx.DiGraph(directed=True)
        # Add vertices and edges to the graph
        for vertex in list(self.vertices_map.values()):
            Graph.add_node(vertex.name, pos=(vertex.x, vertex.y))
            edges = self.edges_map.get_all_edges_of_vertex(vertex)
            for edge in edges:
                Graph.add_edges_from([(edge.origin.name, edge.destination.name)])

        pos = nx.get_node_attributes(Graph, 'pos')
        options = {
            'node_size': 300,
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 16,
        }
        nx.draw(Graph, pos, **options)

    def plot_graph(self):
        self.__get_graph_plot__()
        plt.show()

    def plot_slab_decomposition(self):
        self.__get_graph_plot__()
        plt.axvline(x=0.22058956)
        plt.axvline(x=0.33088437)
        plt.axvline(x=2.20589566)
        # xposition = [0.3, 0.4, 0.45]
        # for xc in xposition:
        #     plt.axvline(x=xc, color='k', linestyle='--')
        plt.show()


if __name__ == "__main__":
    points = [(0, 5), (2, 5), (3, 0), (0, 0)]

    segments = [
        [(0, 5), (2, 5)],
        [(2, 5), (3, 0)],
        [(3, 0), (0, 0)],
        [(0, 0), (0, 5)],
        [(0, 5), (3, 0)],
    ]

    myDCEL = Dcel()
    myDCEL.build_dcel(points, segments)

    #myDCEL.plot_graph()
    myDCEL.plot_slab_decomposition()





