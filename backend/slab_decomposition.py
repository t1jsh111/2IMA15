import backend.visualization as vs


class Slab:
    def __init__(self, begin_x, end_x, edges):
        self.begin_x = begin_x
        self.end_x = end_x
        self.intersecting_edges = self.__get_intersecting_edges(edges)

    def __repr__(self):
        return f"begin_x: {self.begin_x} " + f"end_x: {self.end_x}"

    # Wlog consider the height of the edge at intersection point of end_x line
    def edge_height(self, edge):
        # Edge is not contained in slab
        if edge.destination.x > self.end_x and edge.origin.x >= self.end_x:
            return None
        # Edge is not contained in slab
        if edge.destination.x <= self.begin_x and edge.origin.x < self.begin_x:
            return None

        edge_x_width = edge.destination.x - edge.origin.x
        slope = (edge.destination.y - edge.origin.y) / edge_x_width
        intersection_y = slope * (self.end_x - edge.origin.x) + edge.origin.y

        return intersection_y

    def __get_intersecting_edges(self, edges):
        sorted_edges = []
        for edge in edges:
            height = self.edge_height(edge)
            if height is not None:
                sorted_edges.append((height, edge))
        sorted_edges = sorted(sorted_edges, key = lambda a : a[0])
        return sorted_edges


class SlabDecomposition:
    def __init__(self, dcel):
        self.dcel = dcel
        self.vertices = self.dcel.get_vertices()
        self.slabs = self.get_slabs()

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