from abc import ABC, abstractmethod


# Abstract class for nodes of the trapezoid search tree
class AbstractNode(ABC):
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.parents = {}

    # Breaks the connection from parent to child (WARNING one direction only!)
    # PRE: self.left_node = child_node xor self.right_node = child_node
    # POST: self.left_node = None xor self.right_node = None
    def __detach_child(self, child_node):
        if self.left_child is child_node:
            self.left_child = None
        elif self.right_child is child_node:
            self.right_child = None
        # Pre condition should be harmed if this is reached...
        else:
            Warning

    def add_to_parent_map(self, parent_node):
        self.parents[id(parent_node)] = parent_node

    # Breaks the bidirectional edge connection with the parent via the hash map of parents
    def detach_from_parent(self, node):
        if id(node) in self.parents:
            # Break connection from parent to child
            self.parents[id(node)].__detach_child(self)
            # Break connection from parent to child
            del self.parents[id(node)]

    # Check in constant time if a node is a parent of this
    def has_node_as_parent(self, node):
        return id(node) in self.parents

    # Removes all parents of the item, so that all pointers are removed and Python Garbage Collector
    # Will hopefully delete the item from memory when this node then is out of scope
    def remove_node(self):
        for key, parent in self.parents.items():
            self.detach_from_parent(parent)

    # Function to replace the subtree of which self is the root by a subtree of the provided 'node' argument
    def replace_by_other_node(self, node):
        parents = list(self.parents.values())
        for parent in parents:
            # for each of the parents, the old parent-child connection is broken, and replaced with a connection to node
            parent.replace_child_by(self, node)
        # Probably does not do anything since all parent pointers are already removed.
        self.remove_node()

    # Set the left child of the node and break the child/parent connection that previously existed
    def set_left_child(self, node):
        if self.left_child is not None:
            self.left_child.detach_from_parent(self)
        self.left_child = node
        if node is not None:
            node.add_to_parent_map(self)

    # Set the right child of the node
    def set_right_child(self, node):
        if self.right_child is not None:
            self.right_child.detach_from_parent(self)
        self.right_child = node
        if node is not None:
            node.add_to_parent_map(self)

    # Replace one of the children by the replacement node
    # PRE: self.left_node = child_node xor self.right_node = child_node
    # POST: self.left_node = replacement_node xor self.right_node = replacement_node
    def replace_child_by(self, child_node, replacement_node):
        if self.left_child is child_node:
            self.set_left_child(replacement_node)
        elif self.right_child is child_node:
            self.set_right_child(replacement_node)
        # Pre condition should be harmed if this is reached...
        else:
            raise Exception("Should not occur....")

    @abstractmethod
    def query_for_adding_segment(self, origin_endpoint, added_segment):
        pass

    @abstractmethod
    def query(self, end_point):
        pass

    @abstractmethod
    def get_all_trapezoids(self):
        pass


# Class for the endpoint nodes where endpoints are the ending vertices of the segments
# A left subtree has trapezoids with all x coordinate smaller than the  x-coordinate of this endpoint
# The right subtree has trapezoids for which all x coordinates are greater than the x coordinate of this endpoint.
class EndpointNode(AbstractNode):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super().__init__()

    def __repr__(self):
        return "Endpoint node: " + self.endpoint.__repr__()

    def query_for_adding_segment(self, origin_endpoint, added_segment):
        if origin_endpoint.x < self.endpoint.x:
            return self.left_child.query_for_adding_segment(origin_endpoint, added_segment)
        # if origin_endpoint lies on endpoint, it is treated as lying slightly to the right
        elif origin_endpoint.x >= self.endpoint.x:
            return self.right_child.query_for_adding_segment(origin_endpoint, added_segment)

    def query(self, queried_endpoint):
        if queried_endpoint.x < self.endpoint.x:
            return self.left_child.query(queried_endpoint)
        # if origin_endpoint lies on endpoint, it is treated as lying slightly to the right
        elif queried_endpoint.x >= self.endpoint.x:
            return self.right_child.query(queried_endpoint)

    def get_all_trapezoids(self):
        left_branch = [] if self.left_child is None else self.left_child.get_all_trapezoids()
        right_branch = [] if self.right_child is None else self.right_child.get_all_trapezoids()
        return left_branch + right_branch


# Class for segment nodes
# A left subtree has trapezoids that lie above the segment
# The right subtree has trapezoids that lie below the segment
class SegmentNode(AbstractNode):
    def __init__(self, segment):
        super().__init__()
        self.segment = segment

    def __repr__(self):
        return "Segment node: " + self.segment.__repr__()

    def query_for_adding_segment(self, origin_endpoint, added_segment):
        # Degenerate case
        # Query point lies on edge
        if origin_endpoint.y == self.segment.get_y_at_x(origin_endpoint.x):
            # New segment has higher slope ==> end point lies above self.segment
            if added_segment.get_slope() > self.segment.get_slope():
                return self.left_child.query_for_adding_segment(origin_endpoint, added_segment)
            else:
                return self.right_child.query_for_adding_segment(origin_endpoint, added_segment)
        # query point lies above edge
        elif self.segment.point_lies_above_edge(origin_endpoint):
            return self.left_child.query_for_adding_segment(origin_endpoint, added_segment)
        # Query point lies below edge
        else:
            return self.right_child.query_for_adding_segment(origin_endpoint, added_segment)

    def query(self, end_point):
        if self.segment.point_lies_above_edge(end_point):
            return self.left_child.query(end_point)
        else:
            return self.right_child.query(end_point)

    def get_all_trapezoids(self):
        left_branch = [] if self.left_child is None else self.left_child.get_all_trapezoids()
        right_branch = [] if self.right_child is None else self.right_child.get_all_trapezoids()
        return left_branch + right_branch


# Class for trapezoids: NOTE that it  has a child class trapezoid node. However, one should only make trapezoid objects.
# There should not be multiple trapezoid nodes for a single trapezoid.
# Hence one should create trapezoids, and use the trapezoid_node instead.
class Trapezoid:
    def __init__(self, leftp, rightp, top, bottom):
        self.leftp = leftp
        self.rightp = rightp
        self.top = top
        self.bottom = bottom
        self.lower_right_neighbour = None
        self.upper_right_neighbour = None
        self.upper_left_neighbour = None
        self.lower_left_neighbour = None
        self.trapezoid_node = self.TrapezoidNode(self)

    def __repr__(self):
        return f"\nTrapezoid : leftp: ({self.leftp.x}, {self.leftp.y}), rightp: ({self.rightp.x}, {self.rightp.y}) " \
               f"top: {self.top.__repr__()}, bottom: {self.bottom.__repr__()} "

    def is_intersected_by(self, edge):
        # If Edge lies completely to the right of trapezoid
        if edge.destination.x > self.rightp.x and edge.origin.x >= self.rightp.x:
            return False
        # If Edge lies completely to the left of trapezoid
        if edge.destination.x <= self.leftp.x and edge.origin.x < self.leftp.x:
            return False

    def set_trapezoid_node(self, trapezoid_node):
        self.trapezoid_node = trapezoid_node

    def set_lower_right_neighbour(self, lower_right_neighbour):
        self.lower_right_neighbour = lower_right_neighbour # outside if-clause because we might set neighbour to None
        if lower_right_neighbour is not None:
            lower_right_neighbour.__set_lower_left_neighbour(self)

    def set_upper_right_neighbour(self, upper_right_neighbour):
        self.upper_right_neighbour = upper_right_neighbour # outside if-clause because we might set neighbour to None
        if upper_right_neighbour is not None:
            upper_right_neighbour.__set_upper_left_neighbour(self)

    def __set_lower_left_neighbour(self, lower_left_neighbour):
        self.lower_left_neighbour = lower_left_neighbour

    def __set_upper_left_neighbour(self, upper_left_neighbour):
        self.upper_left_neighbour = upper_left_neighbour

    # NEVER INITIALIZE A TRAPEZOID NODE YOURSELF
    # Only objects of Trapezoid class should be created, and these have a 1-1 relation with a trapezoid node.
    class TrapezoidNode(AbstractNode):
        def __init__(self, trapezoid):
            self.trapezoid = trapezoid
            # Add a bidirectional link between the trapezoid node and the trapezoid itself
            trapezoid.set_trapezoid_node(self)
            super().__init__()

        def __repr__(self):
            return "Trapezoid node: " + self.trapezoid.__repr__()

        def query_for_adding_segment(self, origin_endpoint, added_segment):
            return self

        def query(self, end_point):
            return self

        def get_all_trapezoids(self):
            return [self.trapezoid]