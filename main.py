import dcel as dcel
import slab_decomposition as sd

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

    slab_points = [x for x, y in points]
    slab_points.sort()
    print(slab_points)
    print(myDCEL.edges)

    begin_x = 3
    #slab = Slab(begin_x, slab_points[3], myDCEL.edges)
    #print("Intersecting edges", slab.intersecting_edges)
    # for end_x in slab_points:


    #slab = Slab(points[0][0], points[0])

    #myDCEL.plot_graph()
    #myDCEL.show_dcel()
    slab_decomposition = sd.SlabDecomposition(myDCEL)
    slab_decomposition.show_slab_decomposition()