import backend.visualization as vs
import backend.slabs_bst as bst


class Slab:
    def __init__(self, begin_x, end_x, edges):
        self.begin_x = begin_x
        self.end_x = end_x
        self.intersecting_edges = self.__get_intersecting_edges(edges)

    def __repr__(self):
        return f"begin_x: {self.begin_x} " + f"end_x: {self.end_x}"

    # Return the y-value of the intersection points of the edge with the left- and right boundary of the slab
    def edge_height(self, edge):

        edge_x_width = edge.destination.x - edge.origin.x
        slope = (edge.destination.y - edge.origin.y) / edge_x_width
        intersection_y_right = slope * (self.end_x - edge.origin.x) + edge.origin.y
        intersection_y_left = slope * (self.begin_x - edge.origin.x) + edge.origin.y

        return intersection_y_left, intersection_y_right

    # Returns true if this slab contains the point (x-wise). The left side is considered open and the right side closed
    def contains_point(self, x_coordinate):
        return self.begin_x < x_coordinate <= self.end_x

    # Returns the edges which are contained in the slab, sorted lexicographically on y value of the intersection points
    # of the edges with both boundaries of the slab
    def __get_intersecting_edges(self, edges):
        sorted_edges = []
        for edge in edges:
            # Only consider edges contained in slab
            if not (edge.destination.x > self.end_x and edge.origin.x >= self.end_x) and \
                    not (edge.destination.x <= self.begin_x and edge.origin.x < self.begin_x):
                height_bounds = self.edge_height(edge)
                sorted_edges.append((height_bounds, edge))
        # Sort the edges lexicographically (first on y-value left intersection point slab, and then right
        # intersection point)
        sorted_edges = sorted(sorted_edges, key=lambda a: (a[0][0], a[0][1]))
        return sorted_edges


class SlabDecomposition:
    def __init__(self, dcel):
        self.dcel = dcel
        self.vertices = self.dcel.get_vertices()
        self.slabs = self.get_slabs()
        self.bst_x = bst.create_bst_x(self.slabs)

    # returns a list of slab objects
    def get_slabs(self):
        slabs = []
        slab_points = [vertex.x for vertex in self.vertices]
        slab_points.sort()

        # Each vertex is a begin point of a slab
        begin_x = None
        for end_x in slab_points:
            if begin_x is not None:
                slab = Slab(begin_x, end_x, self.dcel.edges)
                slabs.append(slab)
            begin_x = end_x
        return slabs

    def show_slab_decomposition(self):
        vs.plot_slab_decomposition(self.dcel)

    def solve_for_point(self, x, y):
        slab = bst.slab_tree_search(self.bst_x, x)

        if slab is None:
            return None
        return slab.face_tree_search(slab.bst_y, x, y)

    def show_slab_bst(self):
        vs.plot_binary_search_tree(self.bst_x)
