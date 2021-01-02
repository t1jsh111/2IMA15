from abc import ABC, abstractmethod
import backend.visualization as vs

# Abstract class for nodes of the trapezoid search tree
class AbstractNode(ABC):
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.parents = {}

    # Breaks the connection from parent to child (WARNING one direction only!)
    # PRE: self.left_node = child_node xor self.right_node = child_node
    # POST: self.left_node = None xor self.right_node = None
    def __detach_child(self, child_node):
        if self.left_child is child_node:
            self.left_child = None
        elif self.right_child is child_node:
            self.right_child = None
        # Pre condition should be harmed if this is reached...
        else:
            Warning

    def add_to_parent_map(self, parent_node):
        self.parents[id(parent_node)] = parent_node

    # Breaks the bidirectional edge connection with the parent via the hash map of parents
    def detach_from_parent(self, node):
        if id(node) in self.parents:
            # Break connection from parent to child
            self.parents[id(node)].__detach_child(self)
            # Break connection from parent to child
            del self.parents[id(node)]

    # Check in constant time if a node is a parent of this
    def has_node_as_parent(self, node):
        return id(node) in self.parents

    # Removes all parents of the item, so that all pointers are removed and Python Garbage Collector
    # Will hopefully delete the item from memory when this node then is out of scope
    def remove_node(self):
        for key, parent in self.parents.items():
            self.detach_from_parent(parent)

    # Function to replace the subtree of which self is the root by a subtree of the provided 'node' argument
    def replace_by_other_node(self, node):
        parents = list(self.parents.values())
        for parent in parents:
            # for each of the parents, the old parent-child connection is broken, and replaced with a connection to node
            parent.replace_child_by(self, node)
        # Probably does not do anything since all parent pointers are already removed.
        self.remove_node()

    # Set the left child of the node and break the child/parent connection that previously existed
    def set_left_child(self, node):
        if self.left_child is not None:
            self.left_child.detach_from_parent(self)
        self.left_child = node
        if node is not None:
            node.add_to_parent_map(self)

    # Set the right child of the node
    def set_right_child(self, node):
        if self.right_child is not None:
            self.right_child.detach_from_parent(self)
        self.right_child = node
        if node is not None:
            node.add_to_parent_map(self)

    # Replace one of the children by the replacement node
    # PRE: self.left_node = child_node xor self.right_node = child_node
    # POST: self.left_node = replacement_node xor self.right_node = replacement_node
    def replace_child_by(self, child_node, replacement_node):
        if self.left_child is child_node:
            self.set_left_child(replacement_node)
        elif self.right_child is child_node:
            self.set_right_child(replacement_node)
        # Pre condition should be harmed if this is reached...
        else:
            raise Exception("Should not occur....")

    @abstractmethod
    def query_for_adding_segment(self, origin_endpoint, added_segment):
        pass

    @abstractmethod
    def query(self, end_point):
        pass

    @abstractmethod
    def get_all_trapezoids(self):
        pass


# Class for the endpoint nodes where endpoints are the ending vertices of the segments
# A left subtree has trapezoids with all x coordinate smaller than the  x-coordinate of this endpoint
# The right subtree has trapezoids for which all x coordinates are greater than the x coordinate of this endpoint.
class EndpointNode(AbstractNode):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__()

    def __repr__(self):
        return "Endpoint node: " + self.endpoint.__repr__()

    def query_for_adding_segment(self, origin_endpoint, added_segment):
        if origin_endpoint.x < self.endpoint.x:
            return self.left_child.query_for_adding_segment(origin_endpoint, added_segment)
        elif origin_endpoint.x >= self.endpoint.x:
            return self.right_child.query_for_adding_segment(origin_endpoint, added_segment)

    def query(self, queried_endpoint):
        if queried_endpoint.x < self.endpoint.x:
            return self.left_child.query(queried_endpoint)
        elif queried_endpoint.x >= self.endpoint.x:
            return self.right_child.query(queried_endpoint)

    def get_all_trapezoids(self):
        left_branch = [] if self.left_child is None else self.left_child.get_all_trapezoids()
        right_branch = [] if self.right_child is None else self.right_child.get_all_trapezoids()
        return left_branch + right_branch


# Class for segment nodes
# A left subtree has trapezoids that lie above the segment
# The right subtree has trapezoids that lie below the segment
class SegmentNode(AbstractNode):
    def __init__(self, segment):
        super().__init__()
        self.segment = segment

    def __repr__(self):
        return "Segment node: " + self.segment.__repr__()

    def query_for_adding_segment(self, origin_endpoint, added_segment):
        # Degenerate case
        # Query point lies on edge
        if origin_endpoint.y is self.segment.get_y_at_x(origin_endpoint.x):
            # New segment has higher slope ==> end point lies above self.segment
            if added_segment.get_slope() > self.segment.get_slope():
                return self.left_child.query_for_adding_segment(origin_endpoint, added_segment)
            else:
                return self.right_child.query_for_adding_segment(origin_endpoint, added_segment)
        # query point lies above edge
        elif self.segment.point_lies_above_edge(origin_endpoint):
            return self.left_child.query_for_adding_segment(origin_endpoint, added_segment)
        # Query point lies below edge
        else:
            return self.right_child.query_for_adding_segment(origin_endpoint, added_segment)

    def query(self, end_point):
        if self.segment.point_lies_above_edge(end_point):
            return self.left_child.query(end_point)
        else:
            return self.right_child.query(end_point)

    def get_all_trapezoids(self):
        left_branch = [] if self.left_child is None else self.left_child.get_all_trapezoids()
        right_branch = [] if self.right_child is None else self.right_child.get_all_trapezoids()
        return left_branch + right_branch


# Class for trapezoids: NOTE that it  has a child class trapezoid node. However, one should only make trapezoid objects.
# There should not be multiple trapezoid nodes for a single trapezoid.
# Hence one should create trapezoids, and use the trapezoid_node instead.
class Trapezoid:
    def __init__(self, leftp, rightp, top, bottom):
        self.leftp = leftp
        self.rightp = rightp
        self.top = top
        self.bottom = bottom
        self.lower_right_neighbour = None
        self.upper_right_neighbour = None
        self.upper_left_neighbour = None
        self.lower_left_neighbour = None
        self.trapezoid_node = self.TrapezoidNode(self)

    def __repr__(self):
        return f"\nTrapezoid : leftp: ({self.leftp.x}, {self.leftp.y}), rightp: ({self.rightp.x}, {self.rightp.y}) " \
               f"top: {self.top.__repr__()}, bottom: {self.bottom.__repr__()} "

    def is_intersected_by(self, edge):
        # If Edge lies completely to the right of trapezoid
        if edge.destination.x > self.rightp.x and edge.origin.x >= self.rightp.x:
            return False
        # If Edge lies completely to the left of trapezoid
        if edge.destination.x <= self.leftp.x and edge.origin.x < self.leftp.x:
            return False

    def set_trapezoid_node(self, trapezoid_node):
        self.trapezoid_node = trapezoid_node

    def set_lower_right_neighbour(self, lower_right_neighbour):
        self.lower_right_neighbour = lower_right_neighbour
        if lower_right_neighbour is not None:
            lower_right_neighbour.__set_lower_left_neighbour(self)

    def set_upper_right_neighbour(self, upper_right_neighbour):
        self.upper_right_neighbour = upper_right_neighbour
        if upper_right_neighbour is not None:
            upper_right_neighbour.__set_upper_left_neighbour(self)

    def __set_lower_left_neighbour(self, lower_left_neighbour):
        self.lower_left_neighbour = lower_left_neighbour

    def __set_upper_left_neighbour(self, upper_left_neighbour):
        self.upper_left_neighbour = upper_left_neighbour

    # NEVER INITIALIZE A TRAPEZOID NODE YOURSELF
    # Only objects of Trapezoid class should be created, and these have a 1-1 relation with a trapezoid node.
    class TrapezoidNode(AbstractNode):
        def __init__(self, trapezoid):
            self.trapezoid = trapezoid
            # Add a bidirectional link between the trapezoid node and the trapezoid itself
            trapezoid.set_trapezoid_node(self)
            super().__init__()

        def __repr__(self):
            return "Trapezoid node: " + self.trapezoid.__repr__()

        def query_for_adding_segment(self, origin_endpoint, added_segment):
            return self

        def query(self, end_point):
            return self

        def get_all_trapezoids(self):
            return [self.trapezoid]


class SearchStructure:
    # Expects the initial outer_face trapezoid as argument
    def __init__(self, outer_face):
        self.outer_face_node = outer_face.trapezoid_node
        self.root_node = self.outer_face_node
        return

    # Returns the trapezoid in which the end_point is contained
    def query(self, end_point):
        return self.root_node.query(end_point)

    # Returns the trapezoid in which the end_point is contained
    # Handles degenerate case for adding segment
    # In particular when origin_endpoint.y is the same height as the height of the segment node
    # at the origin_endpoint.x coordinate
    def query_for_adding_segment(self, origin_endpoint, added_segment):
        return self.root_node.query_for_adding_segment(origin_endpoint, added_segment)

    def get_all_trapezoids(self):
        return self.root_node.get_all_trapezoids()

    # See page 131 of the book (and in particular check out figure 6.7)
    def __handle_segment_contained_in_single_trapezoid(self, trapezoid_nodes, segment):
        delta_node = trapezoid_nodes[0]
        delta = delta_node.trapezoid

        pi = EndpointNode(segment.origin)
        qi = EndpointNode(segment.destination)
        si = SegmentNode(segment)

        # Create the trapezoids
        trapezoid_a = Trapezoid(delta.leftp, segment.origin, delta.top, delta.bottom)
        trapezoid_c = Trapezoid(segment.origin, segment.destination, delta.top, segment)
        trapezoid_d = Trapezoid(segment.origin, segment.destination, segment, delta.bottom)
        trapezoid_b = Trapezoid(segment.destination, delta.rightp, delta.top, delta.bottom)

        # Initial trapezoid has no left neighbour
        if delta.upper_left_neighbour is not None:
            delta.upper_left_neighbour.set_upper_right_neighbour(trapezoid_a)
        if delta.lower_left_neighbour is not None:
            delta.lower_left_neighbour.set_lower_right_neighbour(trapezoid_a)
        # Set the neighbours for each of the trapezoids
        trapezoid_a.set_upper_right_neighbour(trapezoid_c)
        trapezoid_a.set_lower_right_neighbour(trapezoid_d)

        trapezoid_c.set_upper_right_neighbour(trapezoid_b)
        # trapezoid_c.set_lower_right_neighbour(trapezoid_b)

        # trapezoid_d.set_upper_right_neighbour(trapezoid_b)
        trapezoid_d.set_lower_right_neighbour(trapezoid_b)

        trapezoid_b.set_upper_right_neighbour(delta.upper_right_neighbour)
        trapezoid_b.set_lower_right_neighbour(delta.lower_right_neighbour)

        # Create connections between the nodes
        pi.set_left_child(trapezoid_a.trapezoid_node)
        pi.set_right_child(qi)
        qi.set_left_child(si)
        qi.set_right_child(trapezoid_b.trapezoid_node)
        si.set_left_child(trapezoid_c.trapezoid_node)
        si.set_right_child(trapezoid_d.trapezoid_node)

        # A,C,D
        if trapezoid_a.leftp != trapezoid_a.rightp and trapezoid_b.leftp == trapezoid_b.rightp:
            # B dissapears, hence neighbour ownership should be transfered accordingly
            trapezoid_c.set_upper_right_neighbour(trapezoid_b.upper_right_neighbour)
            trapezoid_d.set_lower_right_neighbour(trapezoid_b.lower_right_neighbour)

            pi.set_right_child(si)
            subtree_root = pi
        # C,D,B
        elif trapezoid_a.leftp == trapezoid_a.rightp and trapezoid_b.leftp != trapezoid_b.rightp:
            # Trapezoid a disappears, hence the left neighbours  should point accordingly to c and d
            if trapezoid_a.upper_left_neighbour is not None:
                trapezoid_a.upper_left_neighbour.set_upper_right_neighbour(trapezoid_c)
            if trapezoid_a.lower_left_neighbour is not None:
                trapezoid_a.lower_left_neighbour.set_lower_right_neighbour(trapezoid_d)
            subtree_root = qi
        # C,D
        elif trapezoid_a.leftp == trapezoid_a.rightp and trapezoid_b.leftp == trapezoid_b.rightp:
            # B dissapears, hence neighbour ownership should be transfered accordingly
            trapezoid_c.set_upper_right_neighbour(trapezoid_b.upper_right_neighbour)
            trapezoid_d.set_lower_right_neighbour(trapezoid_b.lower_right_neighbour)
            # Trapezoid a disappears, hence the left neighbours  should point accordingly to c and d
            if trapezoid_a.upper_left_neighbour is not None:
                trapezoid_a.upper_left_neighbour.set_upper_right_neighbour(trapezoid_c)
            if trapezoid_a.lower_left_neighbour is not None:
                trapezoid_a.lower_left_neighbour.set_lower_right_neighbour(trapezoid_d)

            subtree_root = si
        # A,B,C,D
        else:
            subtree_root = pi
        if delta_node is self.root_node:
            self.root_node = subtree_root
        else:
            delta_node.replace_by_other_node(subtree_root)

    # Returns from a set of trapezoids and segment, the generated trapezoids that would lie above the segment
    # and returns the generated trapezoids that would lie below the segment
    def __generate_trapezoids_above_and_below_segment(self, trapezoid_nodes, segment):
        upper_trapezoids = []
        lower_trapezoids = []

        first_trapezoid_node = trapezoid_nodes[0]
        first_trapezoid = first_trapezoid_node.trapezoid
        last_trapezoid_node = trapezoid_nodes[-1]
        last_trapezoid = last_trapezoid_node.trapezoid

        last_upper_point = segment.origin
        last_lower_point = segment.origin
        # temporary hack for case 2.2:
        # -------
        old_rightp = last_trapezoid.rightp
        last_trapezoid.rightp = segment.destination
        # -------
        for trapezoid_node in trapezoid_nodes:
            trapezoid = trapezoid_node.trapezoid
            if segment.point_lies_above_edge(trapezoid.rightp):
                new_trapezoid = Trapezoid(last_upper_point, trapezoid.rightp, trapezoid.top, segment)
                # Make the predecessor trapezoid point to this trapezoid
                if len(upper_trapezoids) >= 1:
                    upper_trapezoids[-1].set_lower_right_neighbour(new_trapezoid)
                upper_trapezoids.append(new_trapezoid)
            else:
                new_trapezoid = Trapezoid(last_lower_point, trapezoid.rightp, segment, trapezoid.bottom)
                # Make the predecessor trapezoid point to this trapezoid
                if len(lower_trapezoids) >= 1:
                    lower_trapezoids[-1].set_upper_right_neighbour(new_trapezoid)
                lower_trapezoids.append(new_trapezoid)


        # undo temporary hack:
        # -------
        last_trapezoid.rightp = old_rightp
        # -------
        return (upper_trapezoids, lower_trapezoids)

    def __handle_first_node_in_degenerate_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):
        trapezoid = trapezoid_node.trapezoid
        endpoint_node = EndpointNode(segment.origin)
        begin_trapezoid = Trapezoid(trapezoid.leftp, segment.origin, trapezoid.top, trapezoid.bottom)

        # Fix neighbouring of begin trapezoid
        if trapezoid.upper_left_neighbour is not None:
            trapezoid.upper_left_neighbour.set_upper_right_neighbour(begin_trapezoid)
        if trapezoid.lower_left_neighbour is not None:
            trapezoid.lower_left_neighbour.set_lower_right_neighbour(begin_trapezoid)


        segment_node = SegmentNode(segment)
        trapezoid_above_segment = upper_trapezoids[0]
        trapezoid_below_segment = lower_trapezoids[0]
        segment_node.set_left_child(trapezoid_above_segment.trapezoid_node)
        segment_node.set_right_child(trapezoid_below_segment.trapezoid_node)

        # Make the begin trapezoid point to its right neighbours
        begin_trapezoid.set_upper_right_neighbour(trapezoid_above_segment)
        begin_trapezoid.set_lower_right_neighbour(trapezoid_below_segment)

        endpoint_node.set_left_child(begin_trapezoid.trapezoid_node)
        endpoint_node.set_right_child(segment_node)

        trapezoid_node.replace_by_other_node(endpoint_node)

    def __handle_last_node_in_degenerate_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):
        trapezoid = trapezoid_node.trapezoid
        # Endpoint node (qi)
        endpoint_node = EndpointNode(segment.destination)

        end_trapezoid = Trapezoid(segment.destination, trapezoid.rightp, trapezoid.top, trapezoid.bottom)

        # Transfer ownership of neighbours from old last trapezoid to new end_trapezoid
        end_trapezoid.set_upper_right_neighbour(trapezoid.upper_right_neighbour)
        end_trapezoid.set_lower_right_neighbour(trapezoid.lower_right_neighbour)

        # Segment node (si)
        segment_node = SegmentNode(segment)
        trapezoid_above_segment = upper_trapezoids[-1]
        trapezoid_below_segment = lower_trapezoids[-1]
        segment_node.set_left_child(trapezoid_above_segment.trapezoid_node)
        segment_node.set_right_child(trapezoid_below_segment.trapezoid_node)

        # Transfer ownership of upper trapezoids, to end_trapezoid accordingly
        trapezoid_above_segment.set_upper_right_neighbour(end_trapezoid)
        trapezoid_below_segment.set_lower_right_neighbour(end_trapezoid)

        endpoint_node.set_left_child(segment_node)
        endpoint_node.set_right_child(end_trapezoid.trapezoid_node)

        trapezoid_node.replace_by_other_node(endpoint_node)

    def __handle_node_in_general_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):
        trapezoid_above_segment = upper_trapezoids[0]
        trapezoid_below_segment = lower_trapezoids[0]

        segment_node = SegmentNode(segment)
        segment_node.set_left_child(trapezoid_above_segment)
        segment_node.set_right_child(trapezoid_below_segment)

        trapezoid_node.replace_by_other_node(segment_node)

    def __remove_handled_trapezoid_from_upper_lower_stack(self, trapezoid, upper_trapezoids, lower_trapezoids):
        # Remove the handled trapezoid from the stack
        if trapezoid.rightp == lower_trapezoids[0].rightp:
            lower_trapezoids.pop(0)
        elif trapezoid.rightp == upper_trapezoids[0].rightp:
            upper_trapezoids.pop(0)

    def __handle_first_node_in_general_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):

        trapezoid_above_segment = upper_trapezoids[0]
        trapezoid_below_segment = lower_trapezoids[0]

        # Transfer neighbouring ownership
        if trapezoid_node.upper_left_neighbour is not None:
            trapezoid_node.upper_left_neighbour.set_upper_right_neighbour(trapezoid_above_segment)
        if trapezoid_node.lower_left_neighbour is not None:
            trapezoid_node.lower_left_neighbour.set_lower_right_neighbour(trapezoid_below_segment)

        segment_node = SegmentNode(segment)
        segment_node.set_left_child(trapezoid_above_segment)
        segment_node.set_right_child(trapezoid_below_segment)

        trapezoid_node.replace_by_other_node(segment_node)

    def __handle_last_node_in_general_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):

        trapezoid_above_segment = upper_trapezoids[0]
        trapezoid_below_segment = lower_trapezoids[0]

        # Transfer neighbouring ownership
        trapezoid_above_segment.set_upper_right_neighbour(trapezoid_node.upper_right_neighbour)
        trapezoid_below_segment.set_lower_right_neighbour(trapezoid_node.lower_right_neighbour)

        segment_node = SegmentNode(segment)
        segment_node.set_left_child(trapezoid_above_segment)
        segment_node.set_right_child(trapezoid_below_segment)

        trapezoid_node.replace_by_other_node(segment_node)

    def __handle_segment_contained_in_multiple_trapezoids(self, trapezoid_nodes, segment):
        # CASE 1.1 (general case): segment starts in TrapezoidBegin.leftp
        # CASE 1.2: (degenerate case): segment starts inside Trapezoid1
        # CASE 2.1 (general case): segment ends in TrapezoidLast.rightp
        # CASE 2.2: (degenerate case): segment ends inside TrapezoidLast (split trapezoid in 2)

        # INTERNAL STEP (general case):
        # - trapezoid.rightp above segment ==> use last uppertrapezoid.rightp as left point
        # And generate segment node with left child the new trapezoid, and right child the last uppertrapezoid
        # - trapezoid.rightp below segment ==> use last lowertrapezoid.rightp as left point
        # And generate a segment node with left child the lowertrapezoid and right child the new trapezoid.

        first_trapezoid_node = trapezoid_nodes[0]
        first_trapezoid = first_trapezoid_node.trapezoid
        last_trapezoid_node = trapezoid_nodes[-1]
        last_trapezoid = last_trapezoid_node.trapezoid

        # Case 1.2
        has_degenerate_begin = first_trapezoid.leftp != segment.origin
        # Case 2.2
        has_degenerate_end = last_trapezoid.rightp != segment.destination

        # Step
        (upper_trapezoids, lower_trapezoids) = self.__generate_trapezoids_above_and_below_segment(trapezoid_nodes,
                                                                                                  segment)

        for trapezoid_node in trapezoid_nodes:
            trapezoid = trapezoid_node.trapezoid
            # Case 1.1
            if trapezoid is first_trapezoid and not has_degenerate_begin:
                self.__handle_first_node_in_general_case(trapezoid_node, segment, upper_trapezoids, lower_trapezoids)
            # Case 1.2
            elif trapezoid is first_trapezoid and has_degenerate_begin:
                self.__handle_first_node_in_degenerate_case(trapezoid_node, segment, upper_trapezoids, lower_trapezoids)
            # Case 2.1
            elif trapezoid is last_trapezoid and not has_degenerate_end:
                self.__handle_last_node_in_general_case(trapezoid_node, segment, upper_trapezoids, lower_trapezoids)
            # Case 2.2
            elif trapezoid is last_trapezoid and has_degenerate_end:
                self.__handle_last_node_in_degenerate_case(trapezoid_node, segment, upper_trapezoids, lower_trapezoids)
            # General case
            else:
                self.__handle_node_in_general_case(trapezoid_node, segment, upper_trapezoids, lower_trapezoids)
            self.__remove_handled_trapezoid_from_upper_lower_stack(trapezoid, upper_trapezoids, lower_trapezoids)

    # Pre: trapezoid_nodes is sorted from left to right based on insersection with the segment
    def replace_trapezoid_nodes_for_adding_segment(self, trapezoid_nodes, segment):
        # segment is contained within a single trapezoid
        if len(trapezoid_nodes) == 1:
            self.__handle_segment_contained_in_single_trapezoid(trapezoid_nodes, segment)
        # segment crosses multiple trapezoids
        else:
            self.__handle_segment_contained_in_multiple_trapezoids(trapezoid_nodes, segment)


# class TrapezoidalMap:
#     def __init__(self):
#         return


def follow_segment(search_structure, segment):
    p = segment.origin
    q = segment.destination

    delta_node_0 = search_structure.query_for_adding_segment(p, segment)
    delta_node_j = delta_node_0
    delta_node_list = [delta_node_0]
    # While q lies to the right of rightp
    while q.x > delta_node_j.trapezoid.rightp.x:
        if delta_node_j.trapezoid.rightp.y > segment.get_y_at_x(delta_node_j.trapezoid.rightp.x):
            # delta_node_j_plus_1 = delta_node_j.trapezoid.upper_right_neighbour.trapezoid_node
            delta_node_j_plus_1 = delta_node_j.trapezoid.lower_right_neighbour.trapezoid_node
        else:
            # delta_node_j_plus_1 = delta_node_j.trapezoid.lower_right_neighbour.trapezoid_node
            delta_node_j_plus_1 = delta_node_j.trapezoid.upper_right_neighbour.trapezoid_node
        delta_node_list.append(delta_node_j_plus_1)
        delta_node_j = delta_node_j_plus_1
    return delta_node_list


# Input is the outer_face that is contained in the bounding box...
def trapezoidal_map_algorithm(segments, outer_face):
    outer_face_trapezoid = Trapezoid(outer_face.bottom_left, outer_face.upper_right,
                                     outer_face.top_segment, outer_face.bottom_segment)
    search_structure = SearchStructure(outer_face_trapezoid)
    segment_0 = segments[0]  # segment [o(1,5) d(3,5)]
    intersecting_trapezoid_nodes = follow_segment(search_structure, segment_0)
    search_structure.replace_trapezoid_nodes_for_adding_segment(intersecting_trapezoid_nodes, segment_0)

    # print(intersecting_trapezoid_nodes)
    all_trapezoids = search_structure.get_all_trapezoids()
    print(search_structure.get_all_trapezoids())
    #
    vs.plot_search_structure(search_structure)
    segment_1 = segments[1]
    intersecting_trapezoid_nodes = follow_segment(search_structure, segment_1)
    print(intersecting_trapezoid_nodes)
    search_structure.replace_trapezoid_nodes_for_adding_segment(intersecting_trapezoid_nodes, segment_1)
    vs.plot_search_structure(search_structure)
    trapezoids = search_structure.get_all_trapezoids()
    print(trapezoids)
    segment_2 = segments[2] # edge (1,5)-(4,0)
    intersecting_trapezoid_nodes = follow_segment(search_structure, segment_2)
    print("Intersecting")
    print(intersecting_trapezoid_nodes)
    search_structure.replace_trapezoid_nodes_for_adding_segment(intersecting_trapezoid_nodes, segment_2)
    trapezoids = search_structure.get_all_trapezoids()
    print(trapezoids)



    # segment_3 = segments[3]  # edge (1,5)-(4,0)
    # intersecting_trapezoid_nodes = follow_segment(search_structure, segment_3)
    # search_structure.replace_trapezoid_nodes_for_adding_segment(intersecting_trapezoid_nodes, segment_2)
    # trapezoids = search_structure.get_all_trapezoids()

    # # trapezoidal_map = TrapezoidalMap()
    #
    # for segment in segments:
    #     intersecting_trapezoid_nodes = follow_segment(search_structure, segment)
    #     search_structure.replace_trapezoid_nodes_for_adding_segment(intersecting_trapezoid_nodes, segment)
    #     begin_face = search_structure.query(segment.origin.x)