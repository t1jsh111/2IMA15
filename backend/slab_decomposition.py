import backend.visualization as vs
import backend.slabs_bst as bst


class Slab:
    def __init__(self, begin_x, end_x, edges, is_outer_left):
        self.begin_x = begin_x
        self.end_x = end_x
        self.intersecting_edges = self.__get_intersecting_edges(edges)
        self.is_outer_left_slab = is_outer_left  # For outer left slab the contains_point function needs to be closed on
        # both sides so we cover all points within bounding box

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
        if self.is_outer_left_slab:
            return self.begin_x <= x_coordinate <= self.end_x
        else:
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

        outer_slab_left_begin = self.dcel.outer_face.bottom_left.x
        outer_slab_left_end = slab_points[0]  # Outer slab on the left side starts at left boundary bounding box and
                                              # goes until first vertex
        outer_slab_right_begin = slab_points[-1]
        outer_slab_right_end = self.dcel.outer_face.bottom_right.x

        # Each vertex is a begin point of a slab
        begin_x = None
        for end_x in slab_points:
            if begin_x is not None:
                slab = Slab(begin_x, end_x, self.dcel.edges, False)
                slabs.append(slab)
            begin_x = end_x

        # The only two edges that are going through these slabs are the top and bottom edges of the binary search tree
        outer_edges = [self.dcel.outer_face.bottom_segment, self.dcel.outer_face.top_segment]
        outer_slab_left = Slab(outer_slab_left_begin, outer_slab_left_end, outer_edges, True)
        slabs.append(outer_slab_left)
        outer_slab_right = Slab(outer_slab_right_begin, outer_slab_right_end, outer_edges, False)
        slabs.append(outer_slab_right)

        return slabs

    def show_slab_decomposition(self, query=None):
        if query is not None:
            vs.plot_slab_decomposition(self.dcel, self.slabs, query)
        else:
            vs.plot_slab_decomposition(self.dcel, self.slabs)

    def solve_for_point(self, query, show_bst=None):
        visited_slabs = bst.slab_tree_search(self.bst_x, query.x, [])  # Search for slab
        slab = visited_slabs[-1]  # Last visited slab, which is the slab containing q

        if slab is None:
            return None
        if show_bst:
            self.show_slab_bst(visited_slabs)

        result = slab.face_tree_search(slab.bst_y, query.x, query.y, [])  # Search for face
        visited_edges = result[0]
        face = result[1]

        return slab, visited_edges, face

    def show_slab_bst(self, visited_slabs=None):
        if visited_slabs is not None:
            vs.plot_slab_binary_search_tree(self.bst_x, visited_slabs)
        else:
            vs.plot_slab_binary_search_tree(self.bst_x)

    def get_size(self):
        count = 1
        if self.bst_x.left is not None:
            count += self.__get_size_helper(self.bst_x.left)
        if self.bst_x.right is not None:
            count += self.__get_size_helper(self.bst_x.right)
        return count

    def __get_size_helper(self, node):
        count = 1
        if node.left is not None:
            count += self.__get_size_helper(node.left)
        if node.right is not None:
            count += self.__get_size_helper(node.right)
        return count
