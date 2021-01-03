import backend.dcel as dcel
import backend.slab_decomposition as sd
import complex_algorithm.algorithm as ca


class QueryPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    # =======================================
    # Create DCEL ---------------------------
    # =======================================

    # points = [(1, 5), (3, 5), (4, 0), (1.5, 0)]
    #
    # segments = [
    #     [(1, 5), (3, 5)],
    #     [(3, 5), (4, 0)],
    #     [(4, 0), (1.5, 0)],
    #     [(1.5, 0), (1, 5)],
    #     [(1, 5), (4, 0)],
    # ]
    points = [(1, 5), (3, 5), (4, 0), (1.5, 0), (5, 4)]

    segments = [
        [(1, 5), (3, 5)],
        [(3, 5), (4, 0)],
        [(4, 0), (1.5, 0)],
        [(1.5, 0), (1, 5)],
        [(1, 5), (4, 0)],
        [(3, 5), (5, 4)],
        [(4, 0), (5, 4)],

    ]

    myDCEL = dcel.Dcel()
    myDCEL.build_dcel(points, segments)

    q = QueryPoint(3.5, 4)
    query_point = (3.5, 4)

    # myDCEL.show_dcel()  # Show DCEL without query point
    myDCEL.show_dcel(q)  # Show DCEL with query point

    # =======================================
    # Slab Decomposition --------------------
    # =======================================

    slab_decomposition = sd.SlabDecomposition(myDCEL)

    # slab_decomposition.show_slab_decomposition()  # Show Slab decomposition without query point
    slab_decomposition.show_slab_decomposition(q)  # Show slab decomposition with query point

    # slab_decomposition.show_slab_bst()
    result = slab_decomposition.solve_for_point(q, True)  # True = show bst
    slab = result[0]
    visited_edges = result[1]
    face = result[2]

    if face is None:
        print("None")
    else:
        print(face.name)

    # slab.show_edges_bst()  # Show binary search tree on y-order without marking visited nodes
    # slab.show_edges_bst(visited_edges)  # Show binary search tree on y-order with marking visited nodes

    # =======================================
    # Complex Algorithm- --------------------
    # =======================================

    myDCEL.show_dcel()
    print(myDCEL.get_edges())
    search_structure = ca.trapezoidal_map_algorithm(myDCEL.get_edges(), myDCEL.outer_face)
    search_structure.show_search_structure()
    print(set(search_structure.get_all_trapezoids()))
    t = search_structure.query(q)
    print("-------")
    print("result: " + str(t))
    print("-------")
