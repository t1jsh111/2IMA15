import backend.dcel as dcel
import backend.slab_decomposition as sd

if __name__ == "__main__":
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

    query_point = (1.4, 2)

    #myDCEL.show_dcel()
    myDCEL.show_dcel(query_point[0], query_point[1])

    slab_decomposition = sd.SlabDecomposition(myDCEL)
    print(slab_decomposition.slabs)
    for slab in slab_decomposition.slabs:
        print("Slab with begin_x", slab.begin_x, " and end_x", slab.end_x)
        # print(slab.intersecting_edges)
        for edge in slab.intersecting_edges:
            print("Right edge ", edge[1].right_arrow, " at height (left, right)", edge[0], "with face ",
                  edge[1].right_arrow.incident_face.name, "above it")
        print("------------")

    #slab_decomposition.show_slab_decomposition()
    slab_decomposition.show_slab_decomposition(query_point[0], query_point[1])

    #slab_decomposition.show_slab_bst()

    result = slab_decomposition.solve_for_point(query_point[0], query_point[1], True)
    slab = result[0]
    face = result[1]

    if face is None:
        print("None")
    else:
        print(face.name)

    # ToDo: Overload method for y-bianry search tree in similar way
    # slab.show_edges_bst()
