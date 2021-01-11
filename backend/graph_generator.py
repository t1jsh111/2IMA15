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





# if __name__ == "__main__":
#     create_graph(4)