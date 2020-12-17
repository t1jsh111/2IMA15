import math as m
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


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


class HedgesMap:
    def __init__(self):
        self.origin_destination_map = {}
        self.destination_origin_map = {}

    def insert_hedge(self, origin, destination, hedge):
        self.origin_destination_map.setdefault(origin, {})
        self.origin_destination_map[origin][destination] = hedge

        self.destination_origin_map.setdefault(destination, {})
        self.destination_origin_map[destination][origin] = hedge

    def get_hedge(self, origin, destination):
        return self.origin_destination_map[origin][destination]

    def get_outgoing_hedges(self, origin):
        outgoing_hedges = list(self.origin_destination_map[origin].values())
        return outgoing_hedges

    def get_incoming_hedges(self, destination):
        incoming_hedges = list(self.destination_origin_map[destination].values())
        return incoming_hedges

    # Returns outgoing half edges in clockwise order
    def get_outgoing_hedges_clockwise(self, origin):
        outgoing_hedges = list(self.origin_destination_map[origin].values())
        outgoing_hedges.sort(key = lambda e : e.get_angle(), reverse=True)
        return outgoing_hedges

    # Returns incoming half edges in clockwise order
    def get_incoming_hedges_clockwise(self, destination):
        incoming_hedges = list(self.destination_origin_map[destination].values())
        incoming_hedges.sort(key = lambda e : e.get_angle(), reverse=True)
        return incoming_hedges

    # Returns all the incoming and outgoing half edges
    def get_all_hedges_of_vertex(self, vertex):
        hedges = self.get_incoming_hedges_clockwise(vertex) + self.get_outgoing_hedges(vertex)
        return hedges

    # Returns all hedges of the mapping
    def get_all_hedges(self):
        print(len(list(self.origin_destination_map.values())))
        return list(self.origin_destination_map.values())

    # Deletes half edge from the mapping
    def delete_hedge(self, origin, destination):
        del self.origin_destination_map[origin][destination]
        del self.destination_origin_map[destination][origin]


class Dcel:
    def __init__(self):
        # (x coordinate, y coordinate) -> vertex
        self.vertices_map = {}
        self.hedges_map = HedgesMap()

    def build_dcel(self, points, segments):
        # Creates a hashmap point_coordinates->vertex
        label = 'A'
        for point in points:
            self.vertices_map[point] = Vertex(point[0], point[1], label)
            label = chr(ord(label) + 1)

        # Connects vertices and hedges and assign twins
        for segment in segments:
            origin = self.vertices_map[segment[0]]
            destination = self.vertices_map[segment[1]]

            hedge = HalfEdge(origin, destination)
            twin_hedge = HalfEdge(destination, origin)

            hedge.twin = twin_hedge
            twin_hedge.twin = hedge

            self.hedges_map.insert_hedge(hedge.origin, hedge.destination, hedge)
            self.hedges_map.insert_hedge(twin_hedge.origin, twin_hedge.destination, twin_hedge)

        # Identify next and previous half edges
        for vertex in list(self.vertices_map.values()):
            outgoing_hedges = self.hedges_map.get_outgoing_hedges_clockwise(vertex)
            #print(outgoing_hedges)
            # Consider the outgoing half edges in clockwise order
            # Assign to the twin of each outgoing half edge the next ougoing half edge
            for i in range(len(outgoing_hedges)):
                h1 = outgoing_hedges[i]
                h2 = outgoing_hedges[(i+1) % len(outgoing_hedges)]

                h1.twin.next = h2
                h2.prev = h1.twin

        for a in self.hedges_map.get_all_hedges():
            print(a)
            #print(1)

    def plot_graph(self):
        Graph = nx.DiGraph(directed=True)
        # Add vertices and hedges to the graph
        for vertex in list(self.vertices_map.values()):
            Graph.add_node(vertex.name, pos=(vertex.x, vertex.y))
            hedges = self.hedges_map.get_all_hedges_of_vertex(vertex)
            for hedge in hedges:
                Graph.add_edges_from([(hedge.origin.name, hedge.destination.name)])

        pos = nx.get_node_attributes(Graph, 'pos')
        options = {
            'node_size': 300,
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 16,
        }
        nx.draw(Graph, pos, **options)
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

    myDCEL.plot_graph()





