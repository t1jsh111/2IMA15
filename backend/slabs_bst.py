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

    def show_edges_bst(self, visited_edges=None):
        if visited_edges is not None:
            vs.plot_edges_binary_search_tree(self.bst_y, visited_edges)
        else:
            vs.plot_edges_binary_search_tree(self.bst_y)

    # Search the bst of edges for the face that belongs to query point
    def face_tree_search(self, node, key_x, key_y, visited):
        if node is None:
            return visited  # key not found

        edge = node.edge[1]  # Retrieve the edge object of the node
        y_edge = edge.get_y_at_x(key_x)  # Calculate the y-value of this edge at key_x

        visited.append(node)
        if key_y < y_edge:
            if node.left is None:
                return visited, node.edge[1].left_arrow.incident_face
            return self.face_tree_search(node.left, key_x, key_y, visited)
        elif key_y >= y_edge:
            if node.right is None:
                return visited, node.edge[1].right_arrow.incident_face
            return self.face_tree_search(node.right, key_x, key_y, visited)


# Class represents binary search tree for edges within a slab
class TreeNodeY(object):
    def __init__(self, e):
        self.edge = e
        self.left = None
        self.right = None


# Creates a balanced binary search tree using the slabs sorted on begin_x given as input
def create_bst_x(slabs):
    if not slabs:
        return None
    mid_val = len(slabs) // 2  # Find the middle slab of the sorted list of slabs
    node = TreeNodeX(slabs[mid_val])  # Make the middle slab the root

    # Recurse on left and right part
    node.left = create_bst_x(slabs[:mid_val])
    node.right = create_bst_x(slabs[mid_val + 1:])

    return node


# Search the bst for the slab that belongs to query point
# It returns all slabs visited. Logically then the last slab visited is the slab of the query
def slab_tree_search(node, key, visited):
    if node is None:
        raise Exception("Query point outside bounding box")  # key not found

    visited.append(node)
    if node.slab.contains_point(key) or (node.left is None and node.slab.begin_x == key): # Special case for leftmost slab
        return visited
    elif key <= node.slab.begin_x:
        return slab_tree_search(node.left, key, visited)
    elif key > node.slab.end_x:
        return slab_tree_search(node.right, key, visited)
