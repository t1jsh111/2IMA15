import visualization as vs


class Slab:
    def __init__(self, begin_x, end_x, edges):
        self.begin_x = begin_x
        self.end_x = end_x
        self.intersecting_edges = []
        for edge in edges:
            height = self.edge_height(edge)
            if height is not None:
                self.intersecting_edges.append((height, edge))
        sorted(self.intersecting_edges, key = lambda a : a[0])

    # Wlog consider the height of the edge at intersection point of end_x line
    def edge_height(self, edge):
        # Edge is not contained in slab
        if edge.destination.x > self.end_x and edge.origin.x >= self.end_x:
            return None
        # Edge is not contained in slab
        if edge.destination.x <= self.begin_x and edge.origin.x < self.begin_x:
            return None
        print("edge", edge)
        slope = (edge.destination.y - edge.origin.y) / edge.get_edge_length()
        intersection_y = slope * (self.end_x - self.begin_x) + edge.origin.y
        return intersection_y


class SlabDecomposition:
    def __init__(self, dcel):
        self.dcel = dcel

    def show_slab_decomposition(self):
        vs.plot_slab_decomposition(self.dcel)