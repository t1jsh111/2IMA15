import backend.visualization as vs


# Class represents node of binary search tree for slabs
class TreeNodeX(object):
    def __init__(self, s):
        self.slab = s
        self.bst_y = self.__create_bst_y(self.slab.intersecting_edges)  # intersecting_edges is already in sorted order
        self.left = None
        self.right = None
        self.on_path = False

    def __create_bst_y(self, edges):
        if not edges:
            return None
        mid_val = len(edges) // 2
        node = TreeNodeY(edges[mid_val])
        node.left = self.__create_bst_y(edges[:mid_val])
        node.right = self.__create_bst_y(edges[mid_val + 1:])
        return node

    def show_edges_bst(self):
        vs.plot_edges_binary_search_tree(self.bst_y)

    # Search the face that belongs to query point in binary search tree of edges
    def face_tree_search(self, node, key_x, key_y):
        if node is None:
            return None  # key not found

        edge = node.edge[1]
        y_edge = edge.get_y_at_x(key_x)

        if key_y < y_edge:
            if node.left is None:
                return node.edge[1].left_arrow.incident_face
            return self.face_tree_search(node.left, key_x, key_y)
        elif key_y >= y_edge:
            if node.right is None:
                return node.edge[1].right_arrow.incident_face
            return self.face_tree_search(node.right, key_x, key_y)


# Class represents binary search tree for edges within a slab
class TreeNodeY(object):
    def __init__(self, e):
        self.edge = e
        self.left = None
        self.right = None


# Creates a balanced binary search tree using the slabs given as input
def create_bst_x(slabs):
    if not slabs:
        return None
    slabs = sorted(slabs, key=lambda s: s.begin_x)  # Sort slabs from left to right
    mid_val = len(slabs) // 2
    node = TreeNodeX(slabs[mid_val])
    node.left = create_bst_x(slabs[:mid_val])
    node.right = create_bst_x(slabs[mid_val + 1:])
    return node


# Search the slab that belongs to query point in binary search tree of slabs it returns all slabs visited,
# logically then the last slab visited is the slab of the query
def slab_tree_search(node, key, visited):
    if node is None:
        return visited  # key not found

    if node.slab.contains_point(key) or (node.left is None and node.slab.begin_x == key):
        visited.append(node)
        return visited
    elif key <= node.slab.begin_x:
        visited.append(node)
        return slab_tree_search(node.left, key, visited)
    elif key > node.slab.end_x:
        visited.append(node)
        return slab_tree_search(node.right, key, visited)
