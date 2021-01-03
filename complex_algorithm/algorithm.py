import complex_algorithm.search_tree as st
import complex_algorithm.search_tree_nodes as ds


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


def trapezoidal_map_algorithm(segments, outer_face):
    outer_face_trapezoid = ds.Trapezoid(outer_face.bottom_left, outer_face.upper_right,
                                     outer_face.top_segment, outer_face.bottom_segment)

    # BASE:
    # Search tree is initialized with the outer_face trapezoid
    search_structure = st.SearchStructure(outer_face_trapezoid)

    # TODO: compute a random permutation of segments
    # STEP:
    # Assuming correctness of search structure where segment0-segmenti are added, segmenti+1 is added to the structure
    for segment in segments:
        intersecting_trapezoid_nodes = follow_segment(search_structure, segment) # sorted intersection list
        search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes,
                                                                                   segment)
    return search_structure

# def trapezoidal_map_algorithm(segments, outer_face):
#     outer_face_trapezoid = ds.Trapezoid(outer_face.bottom_left, outer_face.upper_right,
#                                      outer_face.top_segment, outer_face.bottom_segment)
#
#     # BASE:
#     # Search tree is initialized with the outer_face trapezoid
#     search_structure = st.SearchStructure(outer_face_trapezoid)
#
#     # TODO: compute a random permutation of segments
#     # STEP:
#     # Assuming correctness of search structure where segment0-segmenti are added, segmenti+1 is added to the structure
#     segment_0 = segments[0]
#     intersecting_trapezoid_nodes = follow_segment(search_structure, segment_0) # sorted intersection list
#     search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes,
#                                                                                    segment_0)
#     print("segment_0 intersects: ", intersecting_trapezoid_nodes)
#     print("search structure now contains", set(search_structure.get_all_trapezoids()))
#
#     segment_1 = segments[1]
#     intersecting_trapezoid_nodes = follow_segment(search_structure, segment_1)  # sorted intersection list
#     search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes,
#                                                                                segment_1)
#     print("segment_1 intersects: ", intersecting_trapezoid_nodes)
#     print("search structure now contains", set(search_structure.get_all_trapezoids()))
#
#     segment_2 = segments[2]
#     intersecting_trapezoid_nodes = follow_segment(search_structure, segment_2)  # sorted intersection list
#     print("segment_2 intersect")
#     print(intersecting_trapezoid_nodes)
#     search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes, segment_2)
#     print("search structure now contains", set(search_structure.get_all_trapezoids()))
#
#     segment_3 = segments[3]
#     intersecting_trapezoid_nodes = follow_segment(search_structure, segment_3)  # sorted intersection list
#     print("segment_3 intersect")
#     print(intersecting_trapezoid_nodes)
#     search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes, segment_3)
#     print("search structure now contains", set(search_structure.get_all_trapezoids()))
#
#     segment_4 = segments[4]
#     intersecting_trapezoid_nodes = follow_segment(search_structure, segment_4)  # sorted intersection list
#     print("segment_4 intersect")
#     print(intersecting_trapezoid_nodes)
#     search_structure.replace_intersecting_trapezoid_nodes_for_segment_addition(intersecting_trapezoid_nodes, segment_4)
#     print("search structure now contains", set(search_structure.get_all_trapezoids()))

    return search_structure
