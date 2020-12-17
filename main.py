class HalfEdge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vertex ({self.x}, {self.y})"

    def __eq__(self, rhs):
        return self.x is rhs.x and self.y is rhs.y

if __name__ == "__main__" :
    v1 = Vertex(1,2)
    v2 = Vertex(3,4)
    edge = HalfEdge(v1, v2)
    v1.x = 8

    print(edge.origin.x)
