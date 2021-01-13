import vertical_decomposition_algorithm.search_tree as st
import vertical_decomposition_algorithm.search_tree_nodes as ds
import random as random

# Returns the list of trapezoids in the search structure that intersect with segment
# POST: delta_node_list contains all the trapezoids in the search structure that intersect with segment.
#       delta_node_list is sorted on vertical intersection
def follow_segment(search_structure, segment):
    p = segment.origin
    q = segment.destination

    # delta_node_0 is the trapezoid segment.origin lies in
    delta_node_0 = search_structure.query_for_adding_segment(p, segment)
    # Remark: p is the origin of the segment. One might think problems will arrive if
    # p starts on an endpoint. However, this is treated as if it lies slightly to the right.
    # Then the trapezoid in which the segment first "enters" is assigned to delta_node_0
    # This is desired behaviour, as this is indeed what we expect to be the first element of reporting list

    delta_node_j = delta_node_0
    delta_node_list = [delta_node_0]
    # While q lies to the right of rightp
    while q.x > delta_node_j.trapezoid.rightp.x:
        # Delta_j.rightp lies above segment
        if delta_node_j.trapezoid.rightp.y > segment.get_y_at_x(delta_node_j.trapezoid.rightp.x):
            delta_node_j_plus_1 = delta_node_j.trapezoid.lower_right_neighbour.trapezoid_node
        # Delta_j.right lies below segment
        else:
            delta_node_j_plus_1 = delta_node_j.trapezoid.upper_right_neighbour.trapezoid_node
        delta_node_list.append(delta_node_j_plus_1)
        delta_node_j = delta_node_j_plus_1
    return delta_node_list


def trapezoidal_map_algorithm(dcel):
    segments = dcel.get_edges()
    outer_face = dcel.outer_face
    outer_face_trapezoid = ds.Trapezoid(outer_face.bottom_left, outer_face.upper_right,
                                     outer_face.top_segment, outer_face.bottom_segment)

    # BASE:
    # Search tree is initialized with the outer_face trapezoid
    search_structure = st.SearchStructure(outer_face_trapezoid)

    # STEP:
    # Assuming correctness of search structure where segment0-segmenti are added, segmenti+1 is added to the structure
    random.shuffle(segments)
    for segment in segments:
        intersecting_trapezoid_nodes = follow_segment(search_structure, segment) # sorted intersection list
        search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes,
                                                                                   segment)
    trapezoidal_map = st.TrapezoidalMap(dcel, search_structure.get_all_trapezoids())

    return search_structure, trapezoidal_map
