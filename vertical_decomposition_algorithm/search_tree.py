from vertical_decomposition_algorithm.search_tree_nodes import *
import backend.visualization as vs
import collections as col


class TrapezoidalMap():
    def __init__(self, dcel, trapezoids):
        self.trapezoids = list(set(trapezoids))
        self.dcel = dcel

    def get_trapezoids(self):
        return self.trapezoids

    def show_vertical_decomposition(self, query_point=None):
        vs.plot_vertical_decomposition(self.dcel, self.trapezoids, query_point)


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

    def show_search_structure(self):
        vs.plot_search_structure(self)

    # See page 131 of the book (and in particular check out figure 6.7)
    def __handle_segment_contained_in_single_trapezoid(self, trapezoid_nodes, segment):
        covering_trapezoid_node = trapezoid_nodes[0]
        covering_trapezoid = covering_trapezoid_node.trapezoid

        pi = EndpointNode(segment.origin)
        qi = EndpointNode(segment.destination)
        si = SegmentNode(segment)

        # Create the trapezoids
        trapezoid_a = Trapezoid(covering_trapezoid.leftp, segment.origin,
                                covering_trapezoid.top, covering_trapezoid.bottom)
        trapezoid_c = Trapezoid(segment.origin, segment.destination,
                                covering_trapezoid.top, segment)
        trapezoid_d = Trapezoid(segment.origin, segment.destination,
                                segment, covering_trapezoid.bottom)
        trapezoid_b = Trapezoid(segment.destination, covering_trapezoid.rightp,
                                covering_trapezoid.top, covering_trapezoid.bottom)

        covering_trapezoid_has_upper_left_neighbour = covering_trapezoid.upper_left_neighbour is not None
        covering_trapezoid_has_lower_left_neighbour = covering_trapezoid.lower_left_neighbour is not None

        # Move right-neighbour pointers of the left neighbour of covering trapezoid to trapezoid_a
        if covering_trapezoid_has_upper_left_neighbour:
            upper_left_neighbour = covering_trapezoid.upper_left_neighbour
            upper_left_neighbour.set_upper_right_neighbour(trapezoid_a)
        if covering_trapezoid_has_lower_left_neighbour:
            lower_left_neighbour = covering_trapezoid.lower_left_neighbour
            lower_left_neighbour.set_lower_right_neighbour(trapezoid_a)

        # Set the neighbours for each of the trapezoids
        trapezoid_a.set_upper_right_neighbour(trapezoid_c)
        trapezoid_a.set_lower_right_neighbour(trapezoid_d)

        trapezoid_c.set_upper_right_neighbour(trapezoid_b)

        trapezoid_d.set_lower_right_neighbour(trapezoid_b)

        # Move right-neighbour pointers from covering trapezoid to trapezoid_b
        trapezoid_b.set_upper_right_neighbour(covering_trapezoid.upper_right_neighbour)
        trapezoid_b.set_lower_right_neighbour(covering_trapezoid.lower_right_neighbour)

        # Create connections between the nodes as in figure 6.7
        pi.set_left_child(trapezoid_a.trapezoid_node)
        pi.set_right_child(qi)
        qi.set_left_child(si)
        qi.set_right_child(trapezoid_b.trapezoid_node)
        si.set_left_child(trapezoid_c.trapezoid_node)
        si.set_right_child(trapezoid_d.trapezoid_node)

        # Unfortunately figure 6.7 is not the general case
        # A,C,D: When the right-endpoint of middle segment is shared with a different segment
        # C,D,B: When the left-endpoint of middle segment
        #   C,D: When both left and right-endpoint of middle segment are shared
        # Below, we will update the subtree accordingly

        # A,C,D
        if trapezoid_a.leftp != trapezoid_a.rightp and trapezoid_b.leftp == trapezoid_b.rightp:
            # Trapezoid B dissappears: happens only when endpoint of segment are shared
            # Hence the following transfer of neighbour
            trapezoid_c.set_upper_right_neighbour(trapezoid_b.upper_right_neighbour)
            trapezoid_d.set_lower_right_neighbour(trapezoid_b.lower_right_neighbour)

            pi.set_right_child(si)
            subtree_root = pi
        # C,D,B
        elif trapezoid_a.leftp == trapezoid_a.rightp and trapezoid_b.leftp != trapezoid_b.rightp:
            # Trapezoid A dissappears: happens only when endpoint of segment are shared
            # Hence the following transfer of neighbour
            if trapezoid_a.upper_left_neighbour is not None:
                trapezoid_a.upper_left_neighbour.set_upper_right_neighbour(trapezoid_c)
            if trapezoid_a.lower_left_neighbour is not None:
                trapezoid_a.lower_left_neighbour.set_lower_right_neighbour(trapezoid_d)
            subtree_root = qi
        # C,D
        elif trapezoid_a.leftp == trapezoid_a.rightp and trapezoid_b.leftp == trapezoid_b.rightp:
            # Trapezoid B dissappears: happens only when endpoint of segment are shared
            # Hence the following transfer of neighbour
            trapezoid_c.set_upper_right_neighbour(trapezoid_b.upper_right_neighbour)
            trapezoid_d.set_lower_right_neighbour(trapezoid_b.lower_right_neighbour)

            # Trapezoid A dissappears: happens only when endpoint of segment are shared
            # Hence the following transfer of neighbour
            if trapezoid_a.upper_left_neighbour is not None:
                trapezoid_a.upper_left_neighbour.set_upper_right_neighbour(trapezoid_c)
            if trapezoid_a.lower_left_neighbour is not None:
                trapezoid_a.lower_left_neighbour.set_lower_right_neighbour(trapezoid_d)

            subtree_root = si
        # A,B,C,D
        else:
            subtree_root = pi
        # When covering trapezoid was root node, switch it with the subtree root
        if covering_trapezoid_node is self.root_node:
            self.root_node = subtree_root
        # Otherwise, replace node by the subtree root
        else:
            covering_trapezoid_node.replace_by_other_node(subtree_root)

    # Returns from a set of trapezoids and segment, the generated trapezoids that would lie above the segment
    # and returns the generated trapezoids that would lie below the segment
    def __generate_trapezoids_above_and_below_segment(self, intersecting_trapezoid_nodes, segment, has_degenerate_end):
        # INTERNAL STEP (general case):
        # - trapezoid.rightp strictly above segment ==> use last uppertrapezoid.rightp as left point
        # And generate segment node with left child the new trapezoid, and right child the last uppertrapezoid
        # - trapezoid.rightp strictly below segment ==> use last lowertrapezoid.rightp as left point
        # And generate a segment node with left child the lowertrapezoid and right child the new trapezoid.
        #
        # Only scenario where trapezoid.rightp is on segment is in non-degenerate case, for the last segment
        # Otherwise the segment itself would intersect an endpoint of a segment which is not allowed.
        upper_trapezoids = col.deque([])
        lower_trapezoids = col.deque([])

        # Get first and last trapezoid for degenerate case
        last_intersecting_trapezoid_node = intersecting_trapezoid_nodes[-1]
        last_intersecting_trapezoid = last_intersecting_trapezoid_node.trapezoid

        # Keep track of the leftp for the newly generated upper and bottom trapezoids
        # Initially this will be segment.origin, since that point induces the trapezoids above and below the segment
        # Then after generation, it should be set to the newly generated trapezoid.rightp (since that will be the
        # leftp of the future trapezoid).
        # Note that degenerate_begin has no effect on this.
        last_upper_point = segment.origin
        last_lower_point = segment.origin

        # The last trapezoid right_p is special
        # It induces a bottom trapezoid and an upper trapezoid
        # Furthermore in degenerate case it should use segment.destination as rightp for the upper and lower trapezoids
        # Handle intersected trapezoids, except the last trapezoid.
        for intersecting_trapezoid_node in intersecting_trapezoid_nodes[:-1]:
            intersecting_trapezoid = intersecting_trapezoid_node.trapezoid

            if segment.point_lies_above_edge(intersecting_trapezoid.rightp):
                new_upper_trapezoid = Trapezoid(last_upper_point, intersecting_trapezoid.rightp, intersecting_trapezoid.top, segment)
                # Make the predecessor upper trapezoid point to this trapezoid
                if len(upper_trapezoids) >= 1:
                    upper_trapezoids[-1].set_lower_right_neighbour(new_upper_trapezoid)
                upper_trapezoids.append(new_upper_trapezoid)
                last_upper_point = new_upper_trapezoid.rightp
            else:
                new_lower_trapezoid = Trapezoid(last_lower_point, intersecting_trapezoid.rightp, segment, intersecting_trapezoid.bottom)
                # Make the predecessor lower trapezoid point to this trapezoid
                if len(lower_trapezoids) >= 1:
                    lower_trapezoids[-1].set_upper_right_neighbour(new_lower_trapezoid)
                lower_trapezoids.append(new_lower_trapezoid)
                last_lower_point = new_lower_trapezoid.rightp

        # Handle degenerate end
        if has_degenerate_end:
            new_upper_trapezoid = Trapezoid(last_upper_point, segment.destination,
                                            last_intersecting_trapezoid.top, segment)
            if len(upper_trapezoids) >= 1:
                upper_trapezoids[-1].set_lower_right_neighbour(new_upper_trapezoid)
            upper_trapezoids.append(new_upper_trapezoid)

            new_lower_trapezoid = Trapezoid(last_lower_point, segment.destination,
                                            segment, last_intersecting_trapezoid.bottom)
            if len(lower_trapezoids) >= 1:
                lower_trapezoids[-1].set_upper_right_neighbour(new_lower_trapezoid)
            lower_trapezoids.append(new_lower_trapezoid)
        # Handle non-degenerate end
        else:
            new_upper_trapezoid = Trapezoid(last_upper_point, last_intersecting_trapezoid.rightp,
                                            last_intersecting_trapezoid.top, segment)
            if len(upper_trapezoids) >= 1:
                upper_trapezoids[-1].set_lower_right_neighbour(new_upper_trapezoid)
            upper_trapezoids.append(new_upper_trapezoid)

            new_lower_trapezoid = Trapezoid(last_lower_point, last_intersecting_trapezoid.rightp,
                                            segment, last_intersecting_trapezoid.bottom)
            if len(lower_trapezoids) >= 1:
                lower_trapezoids[-1].set_upper_right_neighbour(new_lower_trapezoid)
            lower_trapezoids.append(new_lower_trapezoid)
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

        # Transfer ownership of neighbours from old last_trapezoid to new last_trapezoid
        end_trapezoid.set_upper_right_neighbour(trapezoid.upper_right_neighbour)
        end_trapezoid.set_lower_right_neighbour(trapezoid.lower_right_neighbour)

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
        segment_node.set_left_child(trapezoid_above_segment.trapezoid_node)
        segment_node.set_right_child(trapezoid_below_segment.trapezoid_node)

        trapezoid_node.replace_by_other_node(segment_node)

    def __remove_handled_trapezoid_from_upper_lower_stack(self, trapezoid, upper_trapezoids, lower_trapezoids):
        # Remove the handled trapezoid from the stack
        if trapezoid.rightp == lower_trapezoids[0].rightp:
            lower_trapezoids.popleft()
        elif trapezoid.rightp == upper_trapezoids[0].rightp:
            upper_trapezoids.popleft()

    def __handle_first_node_in_general_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):

        trapezoid_above_segment = upper_trapezoids[0]
        trapezoid_below_segment = lower_trapezoids[0]

        # Transfer neighbouring ownership
        if trapezoid_node.trapezoid.upper_left_neighbour is not None:
            trapezoid_node.trapezoid.upper_left_neighbour.set_upper_right_neighbour(trapezoid_above_segment)
        if trapezoid_node.trapezoid.lower_left_neighbour is not None:
            trapezoid_node.trapezoid.lower_left_neighbour.set_lower_right_neighbour(trapezoid_below_segment)

        segment_node = SegmentNode(segment)
        segment_node.set_left_child(trapezoid_above_segment.trapezoid_node)
        segment_node.set_right_child(trapezoid_below_segment.trapezoid_node)

        trapezoid_node.replace_by_other_node(segment_node)

    def __handle_last_node_in_general_case(self, trapezoid_node, segment, upper_trapezoids, lower_trapezoids):

        trapezoid_above_segment = upper_trapezoids[0]
        trapezoid_below_segment = lower_trapezoids[0]

        # Transfer neighbouring ownership
        trapezoid_above_segment.set_upper_right_neighbour(trapezoid_node.trapezoid.upper_right_neighbour)
        trapezoid_below_segment.set_lower_right_neighbour(trapezoid_node.trapezoid.lower_right_neighbour)

        segment_node = SegmentNode(segment)
        segment_node.set_left_child(trapezoid_above_segment.trapezoid_node)
        segment_node.set_right_child(trapezoid_below_segment.trapezoid_node)

        trapezoid_node.replace_by_other_node(segment_node)

    def __handle_segment_contained_in_multiple_trapezoids(self, intersecting_trapezoid_nodes, segment):
        #
        # CASE 1.1 (general case): segment starts in first_trapezoid.leftp
        # CASE 1.2: (degenerate case): segment starts inside first_trapezoid (split first trapezoid in 2)
        # CASE 2.1 (general case): segment ends in last_trapezoid.rightp
        # CASE 2.2: (degenerate case): segment ends inside last_trapezoid (split trapezoid in 2)

        # INTERNAL STEP (general case):
        # - trapezoid.rightp strictly above segment ==> use last uppertrapezoid.rightp as left point
        # And generate segment node with left child the new trapezoid, and right child the last uppertrapezoid
        # - trapezoid.rightp strictly below segment ==> use last lowertrapezoid.rightp as left point
        # And generate a segment node with left child the lowertrapezoid and right child the new trapezoid.
        #
        # Note that these strict cases are exhaustive. If trapezoid.rightp would lie on segment

        first_intersecting_trapezoid_node = intersecting_trapezoid_nodes[0]
        last_intersecting_trapezoid_node = intersecting_trapezoid_nodes[-1]
        first_trapezoid = first_intersecting_trapezoid_node.trapezoid
        last_trapezoid = last_intersecting_trapezoid_node.trapezoid

        # Case 1.2 holds
        has_degenerate_begin = first_trapezoid.leftp != segment.origin
        # Case 2.2 holds
        has_degenerate_end = last_trapezoid.rightp != segment.destination

        # Step
        (upper_trapezoids, lower_trapezoids) = self.__generate_trapezoids_above_and_below_segment(
            intersecting_trapezoid_nodes, segment, has_degenerate_end)

        for trapezoid_node in intersecting_trapezoid_nodes:
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

    # Pre: trapezoid_nodes is sorted from left to right based on intersection with the segment
    def replace_intersecting_trapezoid_nodes_for_segment_addition(self, intersecting_trapezoid_nodes, segment):
        # Segment is contained within a single trapezoid
        if len(intersecting_trapezoid_nodes) == 1:
            self.__handle_segment_contained_in_single_trapezoid(intersecting_trapezoid_nodes, segment)
        # Segment crosses multiple trapezoids
        else:
            self.__handle_segment_contained_in_multiple_trapezoids(intersecting_trapezoid_nodes, segment)

    def get_size(self):
        node = self.root_node
        visited_nodes = [node]
        count, visited_nodes = self.__walk_searchstructure_count(node, visited_nodes)
        count = 1 + count
        return count

    # Helper method for counting the number of nodes of the search structure
    def __walk_searchstructure_count(self, node, visited_nodes):
        c1 = 0
        c2 = 0
        if node.left_child is not None:
            if node.left_child not in visited_nodes:
                visited_nodes.append(node.left_child)
                c1, visited_nodes = self.__walk_searchstructure_count(node.left_child, visited_nodes)
                c1 += 1
            else:
                c1, visited_nodes = self.__walk_searchstructure_count(node.left_child, visited_nodes)
        if node.right_child is not None:
            if node.right_child not in visited_nodes:
                visited_nodes.append(node.right_child)
                c2, visited_nodes = self.__walk_searchstructure_count(node.right_child, visited_nodes)
                c2 += 1
            else:
                c2, visited_nodes = self.__walk_searchstructure_count(node.right_child, visited_nodes)
        count = c1 + c2
        return count, visited_nodes

