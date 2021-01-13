from random import randrange


# Create pyramid like expanding graph
def create_expanding_graph(number_of_faces):
    number_of_segments = number_of_faces+1

    last_right_coordinate = (1, 0)
    last_left_coordinate = (-1, 0)
    vertices = [last_right_coordinate, last_left_coordinate]
    segments = [[last_left_coordinate, last_right_coordinate]]

    for i in range(number_of_segments-1):
        new_left_coordinate = (last_left_coordinate[0] - 1, last_left_coordinate[1] + 1)
        new_right_coordinate = (last_right_coordinate[0]+1, last_right_coordinate[1]+1)
        vertices.append(new_left_coordinate)
        vertices.append(new_right_coordinate)

        vertices.append(new_left_coordinate)
        vertices.append(new_right_coordinate)

        segments.append([new_left_coordinate, new_right_coordinate])
        segments.append([last_left_coordinate, new_left_coordinate])
        segments.append([last_right_coordinate, new_right_coordinate])

        last_right_coordinate = new_right_coordinate
        last_left_coordinate = new_left_coordinate
    return vertices, segments


# Create v-structured graph that expands horizontally
def create_horizontal_graph(number_of_edges):
    if number_of_edges <= 2:
        raise Exception("Input more than 2 edges expected")
    vertices = []
    segments = []

    # Initialize first 2 points and segments
    prev_point_high = (0, 4)
    prev_point_low = (2, 0)
    vertices.append(prev_point_high)
    vertices.append(prev_point_low)
    segments.append([prev_point_high, prev_point_low])

    created_vertices_high = 1
    created_vertices_low = 1

    while (len(segments)) < number_of_edges:

        created_vertices_total = created_vertices_low + created_vertices_high

        if created_vertices_total % 2 == 0:
            point = (0 + (created_vertices_high * 4), 4)
            vertices.append(point)

            segments.append([prev_point_high, point])

            # If this point is the last segment created it must have an edge to lower previous point
            # If not we have a random chance of adding this segment to result in different structures
            if len(segments) == (number_of_edges - 1) or (randrange(2) == 1 and len(segments) <= (number_of_edges - 3)):
                segments.append([prev_point_low, point])

            prev_point_high = point
            created_vertices_high += 1
        else:
            point = (2 + (created_vertices_low * 4), 0)
            vertices.append(point)

            segments.append([prev_point_low, point])

            # If this point is the last segment created it must have an edge to lower previous point
            # If not we have a random chance of adding this segment to result in different structures
            if len(segments) == (number_of_edges - 1) or (randrange(2) == 1 and len(segments) <= (number_of_edges - 3)):
                segments.append([prev_point_high, point])

            prev_point_low = point
            created_vertices_low += 1
    return vertices, segments
