from random import randrange


def create_graph(number_of_vertices):
    if number_of_vertices <= 2:
        raise Exception("Input more than 2 vertices expected")
    vertices = []
    segments = []

    prev_point_high = (0, 4)
    prev_point_low = (2, 0)
    vertices.append(prev_point_high)
    vertices.append(prev_point_low)
    segments.append([prev_point_high, prev_point_low])
    created_vertices_high = 1
    created_vertices_low = 1

    while (created_vertices_low + created_vertices_high) < number_of_vertices:

        created_vertices_total = created_vertices_low + created_vertices_high

        if created_vertices_total % 2 == 0:
            point = (0 + (created_vertices_high * 4), 4)
            vertices.append(point)

            segments.append([prev_point_high, point])

            # If this point is the last point created it must have an edge to lower previous point
            # If not we have a random chance of adding this segment to result in different structures
            if created_vertices_total == number_of_vertices - 1 or randrange(2) == 1:
                segments.append([prev_point_low, point])

            prev_point_high = point
            created_vertices_high += 1
        else:
            point = (2 + (created_vertices_low * 4), 0)
            vertices.append(point)

            segments.append([prev_point_low, point])

            # If this point is the last point created it must have an edge to lower previous point
            # If not we have a random chance of adding this segment to result in different structures
            if created_vertices_total == number_of_vertices - 1 or randrange(2) == 1:
                segments.append([prev_point_high, point])

            prev_point_low = point
            created_vertices_low += 1

    print(vertices)
    print(segments)
    return vertices, segments
