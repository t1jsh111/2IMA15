import backend.dcel as dcel
import backend.slab_decomposition as sd
import backend.complex_algorithm as ca

if __name__ == "__main__":
    points = [(1, 5), (3, 5), (4, 0), (1.5, 0)]

    segments = [
        [(1, 5), (3, 5)],
        [(3, 5), (4, 0)],
        [(4, 0), (1.5, 0)],
        [(1.5, 0), (1, 5)],
        [(1, 5), (4, 0)],
    ]

    myDCEL = dcel.Dcel()
    myDCEL.build_dcel(points, segments)
    #myDCEL.show_dcel()
    print(myDCEL.get_edges())
    ca.trapezoidal_map_algorithm(myDCEL.get_edges(), myDCEL.outer_face)


    # slab_points = [x for x, y in points]
    # slab_points.sort()
    # print(slab_points)
    # print(myDCEL.edges)
    #
    # begin_x = 3
    # #slab = Slab(begin_x, slab_points[3], myDCEL.edges)
    # #print("Intersecting edges", slab.intersecting_edges)
    # # for end_x in slab_points:
    #
    #
    # #slab = Slab(points[0][0], points[0])
    #
    # #myDCEL.plot_graph()
    # #myDCEL.show_dcel()
    # slab_decomposition = sd.SlabDecomposition(myDCEL)
    # print(slab_decomposition.slabs)
    # for slab in slab_decomposition.slabs:
    #     print("Slab with begin_x", slab.begin_x, " and end_x", slab.end_x)
    #     # print(slab.intersecting_edges)
    #     for edge in slab.intersecting_edges:
    #         print("Right edge ", edge[1].right_arrow, " at height (left, right)", edge[0], "with face ", edge[1].right_arrow.incident_face.name, "above it")
    #     print("------------")
    #
    # slab_decomposition.show_slab_decomposition()
