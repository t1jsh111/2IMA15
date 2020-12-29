import math as m
import backend.visualization as vs
from shapely.geometry import Polygon

class Face:
    def __init__(self):
        self.name = None
        self.outer_component = None  # One half edge of the outer-cycle
        self.isMax = False  # If all edges are connected, the hedges of the max face define the inner boundary of the outer face

    def __repr__(self):
        return f"Face : (n[{self.name}], outer[{self.outer_component.origin.x}, {self.outer_component.origin.y}])"

    def __eq__(self, rhs):
        return self.name is rhs.name and self.name is rhs.name


class HalfEdge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.incident_face = None
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


class Edge:
    def __init__(self, half_edge1, half_edge2):
        if half_edge1.destination.x > half_edge2.destination.x:
            self.right_arrow = half_edge1
            self.left_arrow = half_edge2
        else:
            self.right_arrow = half_edge2
            self.left_arrow = half_edge1

        self.origin = self.right_arrow.origin
        self.destination = self.right_arrow.destination

    def __repr__(self):
        return f"right_arrow [({self.right_arrow.origin.x}, {self.right_arrow.origin.y}), " \
               f"({self.right_arrow.destination.x}, {self.right_arrow.destination.y})], " \
               f"left_arrow [({self.left_arrow.origin.x}, {self.left_arrow.origin.y}), " \
               f"({self.left_arrow.destination.x}, {self.left_arrow.destination.y})]"

    def get_y_at_x(self, x):
        # In case the x coordinate lies outside of the range of the line return None
        if x < self.origin.x or x > self.destination.x:
            return None

        edge_x_width = self.destination.x - self.origin.x
        slope = (self.destination.y - self.origin.y) / edge_x_width
        y_at_x = slope * (x - self.origin.x) + self.origin.y
        return y_at_x

    def get_edge_length(self):
        return self.right_arrow.get_length()


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
        all_hedges = []
        for key, hedges_dic in self.origin_destination_map.items():
            all_hedges = all_hedges + (list(hedges_dic.values()))
        return all_hedges

    # Deletes half edge from the mapping
    def delete_hedge(self, origin, destination):
        del self.origin_destination_map[origin][destination]
        del self.destination_origin_map[destination][origin]


class Dcel:
    def __init__(self):
        # (x coordinate, y coordinate) -> vertex
        self.vertices_map = {}
        self.hedges_map = HedgesMap()
        self.faces = []
        self.edges = []

    def build_dcel(self, points, segments):
        self.__add_points(points)
        self.__add_edges_and_twins(segments)
        self.__add_next_and_previous_pointers()
        self.__add_face_pointers()

    def show_dcel(self):
        vs.plot_graph(self)

    def get_vertices(self):
        return list(self.vertices_map.values())

    def __add_points(self, points):
        # Creates a hashmap (x coordinate, y coordinate) -> vertex
        label = 'A'
        for point in points:
            self.vertices_map[point] = Vertex(point[0], point[1], label)
            label = chr(ord(label) + 1)

    def __add_edges_and_twins(self, segments):
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

            self.edges.append(Edge(hedge, twin_hedge))

    def __add_next_and_previous_pointers(self):
        # Identify next and previous half edges
        for vertex in list(self.vertices_map.values()):
            outgoing_hedges = self.hedges_map.get_outgoing_hedges_clockwise(vertex)
            # Consider the outgoing half edges in clockwise order
            # Assign to the twin of each outgoing half edge the next ougoing half edge
            for i in range(len(outgoing_hedges)):
                h1 = outgoing_hedges[i]
                h2 = outgoing_hedges[(i+1) % len(outgoing_hedges)]

                h1.twin.next = h2
                h2.prev = h1.twin

    def __add_face_pointers(self):
        # Create a face for every cycle of half edges
        number_of_faces = 0
        max_face = None
        max_face_area = 0
        for hedge in self.hedges_map.get_all_hedges():
            if hedge.incident_face is None:  # If this half edge has no incident face yet
                vertex_list = []
                vertex_list.append((hedge.origin.x, hedge.origin.y))

                face_size = 1
                number_of_faces += 1

                f = Face()
                f.name = "f" + str(number_of_faces)

                f.outer_component = hedge
                hedge.incident_face = f

                h = hedge
                while not h.next == hedge:  # Walk through all hedges of the cycle and set incident face
                    h.incident_face = f
                    h = h.next
                    face_size += 1
                    vertex_list.append((h.origin.x, h.origin.y))
                h.incident_face = f

                self.faces.append(f)



                # Calculate area of face formed by the half-edges
                polygon = Polygon(vertex_list)
                if polygon.area > max_face_area:  # Find largest face
                    max_face_area = polygon.area
                    max_face = f

        max_face.isMax = True


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





