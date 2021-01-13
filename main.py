import backend.dcel as dcel
import slab_decomposition_algorithm.slab_decomposition as sd
import vertical_decomposition_algorithm.algorithm as ca
import graph_generation.graph_generator as generator


class QueryPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == "__main__":
    # =======================================
    # Create DCEL ---------------------------
    # =======================================

    # Example planar subdivision input 1 (comment out if not needed)
    points = [(1, 5), (3, 5), (4, 0), (1.5, 0)]

    segments = [
        [(1, 5), (3, 5)],
        [(3, 5), (4, 0)],
        [(4, 0), (1.5, 0)],
        [(1.5, 0), (1, 5)],
        [(1, 5), (4, 0)],
    ]

    # Example planar subdivision input 2 (comment out if not needed)
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
    # =======================================
    # Cases Generator -----------------------
    # =======================================
    # Generation of test case 1 planar subdivision (comment out if not needed)
    # points, segments = generator.create_expanding_graph(5)

    # Generation of test case 2 planar subdivision (comment out if not needed)
    # points, segments = generator.create_horizontal_graph(20)

    myDCEL = dcel.Dcel()
    myDCEL.build_dcel(points, segments)

    q = QueryPoint(3.25, 2)     # Initialise query point

    myDCEL.show_dcel()          # Show DCEL without query point
    # myDCEL.show_dcel(q)       # Show DCEL with query point

    # =======================================
    # Slab Decomposition --------------------
    # =======================================
    slab_decomposition = sd.SlabDecomposition(myDCEL)

    # slab_decomposition.show_slab_decomposition()          # Show Slab decomposition without query point
    # slab_decomposition.show_slab_decomposition(q)         # Show slab decomposition with query point

    slab_decomposition.show_slab_bst()                      # Show binary search tree of slabs
    result = slab_decomposition.solve_for_point(q, False)   # True = show bst
    slab = result[0]
    visited_edges = result[1]
    face = result[2]

    print("------- Slab decomposition -------")
    if face is None:
        print("face: None")
    else:
        print("face: " + str(face.name))
    print("----------------------------------")

    slab.show_edges_bst()               # Show binary search tree on y-order without marking visited nodes
    slab.show_edges_bst(visited_edges)  # Show binary search tree on y-order with marking visited nodes

    # # =======================================
    # # Vertical Decomposition ----------------
    # # =======================================

    search_structure, trapezoidal_map = ca.trapezoidal_map_algorithm(myDCEL)
    search_structure.show_search_structure()    # Show search tree for vertical decomposition

    t = search_structure.query(q).trapezoid     # Trapezoid containing query point q
    face = t.bottom.right_arrow.incident_face   # Face in which trapezoid lies

    print("----- Vertical decomposition -----")
    if face is None:
        print("face: None")
    else:
        print("face: " + str(face.name))
    print("----------------------------------")

    trapezoidal_map.show_vertical_decomposition()   # Plot vertical decomposition on current DCEL
