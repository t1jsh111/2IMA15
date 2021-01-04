import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random as r

NODE_COLOR = 'steelblue'
QUERY_COLOR = 'red'
QUERY_NAME = 'query'

plt.rcParams['figure.figsize'] = [10, 5]


def __draw_graph(dcel, query=None):
    Graph = nx.DiGraph(directed=True)
    # pos = []
    # Add vertices and hedges to the graph
    if query is not None:
        Graph.add_node(QUERY_NAME, pos=(query.x, query.y))

    for vertex in list(dcel.vertices_map.values()):
        Graph.add_node(vertex.name, pos=(vertex.x, vertex.y))
        hedges = dcel.hedges_map.get_all_hedges_of_vertex(vertex)
        for hedge in hedges:
            Graph.add_edges_from([(hedge.origin.name, hedge.destination.name)])

    color_map = []
    for node in Graph:
        if node == QUERY_NAME:
            color_map.append(QUERY_COLOR)
        else:
            color_map.append(NODE_COLOR)

    pos = nx.get_node_attributes(Graph, 'pos')
    labels = {}
    for vertex_name, vertex_location in pos.items():
        labels[vertex_name] = f"{vertex_name}: " + f"{vertex_location}"
    options = {
        'node_size': 400,
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 20,
        'with_labels': True,
        'node_color': color_map,
        'labels': labels,
        'font_weight': 'bold',
        'font_color': 'black',
        'font_size': 15,
        'connectionstyle': 'bar, fraction = 0',
        'verticalalignment': 'bottom'
    }
    nx.draw(Graph, pos, **options)
    # plt.axvline(x=2)
    # plt.scatter(2, 5, marker=".", s=200)
    return Graph


# Colors every face (except outer face) in a random color
def __color_faces(dcel):
    for f in dcel.faces:
        if not f.isMax:
            vertex_list = []

            start_hedge = f.outer_component
            vertex_list.append((start_hedge.origin.x, start_hedge.origin.y))

            h = start_hedge
            while not h.next == start_hedge:
                h = h.next
                vertex_list.append((h.origin.x, h.origin.y))

            polygon = plt.Polygon(vertex_list, color=[r.random(), r.random(), r.random()], alpha=0.5, label=f.name)
            plt.gca().add_patch(polygon)
            plt.legend(loc='upper right')


def plot_graph(dcel, query=None):
    __color_faces(dcel)

    if query is not None:
        __draw_graph(dcel, query)
    else:
        __draw_graph(dcel)
    plt.xlim(plt.xlim()[0] - 0.7, plt.xlim()[1] + 0.7)  # Add margins for labels and text around the edges
    plt.show()


def plot_slab_decomposition(dcel, query=None):
    __color_faces(dcel)
    for vertex in list(dcel.vertices_map.values()):
        plt.axvline(x=vertex.x, color='green', linewidth=3)
    if query is not None:
        __draw_graph(dcel, query)
    else:
        __draw_graph(dcel)
    __draw_graph(dcel)
    plt.xlim(plt.xlim()[0] - 0.7, plt.xlim()[1] + 0.7)  # Add margins for labels and text around the edges
    plt.show()


def __draw_trapezoid(trapezoid):
    left_x = trapezoid.leftp.x


    right_x = trapezoid.rightp.x
    left_segment_bottom_endpoint = (left_x, trapezoid.bottom.get_y_at_x(left_x))
    left_segment_top_endpoint = (left_x, trapezoid.top.get_y_at_x(left_x))

    right_segment_bottom_endpoint = (right_x, trapezoid.bottom.get_y_at_x(right_x))
    right_segment_top_endpoint = (right_x, trapezoid.top.get_y_at_x(right_x))

    plt.plot([left_x, left_x], [trapezoid.bottom.get_y_at_x(left_x), trapezoid.top.get_y_at_x(left_x)])


def plot_vertical_decomposition(dcel, trapezoids):
    __color_faces(dcel)
    # draw trapezoid
    for trapezoid in trapezoids:
        left_x = trapezoid.leftp.x
        plt.plot([left_x, left_x], [trapezoid.bottom.get_y_at_x(left_x), trapezoid.top.get_y_at_x(left_x)])
        __draw_trapezoid(trapezoid)
    last_trapezoid = trapezoids[-1]
    right_x = last_trapezoid.rightp.x
    plt.plot([right_x, right_x], [last_trapezoid.bottom.get_y_at_x(right_x), last_trapezoid.top.get_y_at_x(left_x)])

    __draw_graph(dcel)
    plt.show()


def plot_slab_binary_search_tree(root_node, visited=None):
    Graph = nx.DiGraph(directed=True)

    node = root_node
    Graph.add_node(node.slab, pos=(0, 0))
    __walk_tree_slab(Graph, node, 0, 0)

    node_color_map = []
    for node in Graph:
        if visited is not None and any(v.slab == node for v in visited):
            node_color_map.append(QUERY_COLOR)
        else:
            node_color_map.append(NODE_COLOR)

    edge_color_map = []
    for e in Graph.edges():
        # edge is mapped to QUERY_COLOR color if both of it's endpoints are visited
        if visited is not None and any(v.slab == e[0] for v in visited) and any(v.slab == e[1] for v in visited):
            edge_color_map.append(QUERY_COLOR)
        else:
            edge_color_map.append(NODE_COLOR)

    pos = nx.get_node_attributes(Graph, 'pos')
    labels = {}
    for slab in Graph.nodes():
        labels[slab] = "slab[" + f"{slab.begin_x}: " + f"{slab.end_x}" + "]"
    options = {
        'node_size': 400,
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 20,
        'with_labels': True,
        'node_color': node_color_map,
        'edge_color': edge_color_map,
        'labels': labels,
        'font_weight': 'bold',
        'font_color': 'black',
        'font_size': 15,
        'connectionstyle': 'bar, fraction = 0',
        'verticalalignment': 'bottom'
    }
    nx.draw(Graph, pos, **options)
    plt.xlim(plt.xlim()[0] - 0.5, plt.xlim()[1] + 0.5)  # Add margin to make sure binary search tree is fully visible
    plt.show()


# Helper method for iterating over binary search tree
def __walk_tree_slab(g, n, prev_x, level):
    level = level + 1
    if n.left is not None:
        min_x = prev_x - 1
        g.add_node(n.left.slab, pos=(min_x, -level))
        g.add_edge(n.slab, n.left.slab)
        __walk_tree_slab(g, n.left, min_x, level)

    if n.right is not None:
        max_x = prev_x + 1
        g.add_node(n.right.slab, pos=(max_x, -level))
        g.add_edge(n.slab, n.right.slab)
        __walk_tree_slab(g, n.right, max_x, level)


def plot_edges_binary_search_tree(root_node, visited=None):
    Graph = nx.DiGraph(directed=True)

    node = root_node
    Graph.add_node(node.edge, pos=(0, 0))
    __walk_tree_edges(Graph, node, 0, 0)

    node_color_map = []
    for node in Graph:
        if visited is not None and any(v.edge == node for v in visited):
            node_color_map.append(QUERY_COLOR)
        else:
            node_color_map.append(NODE_COLOR)

    edge_color_map = []
    for e in Graph.edges():
        # edge is mapped to QUERY_COLOR color if both of it's endpoints are visited
        if visited is not None and any(v.edge == e[0] for v in visited) and any(v.edge == e[1] for v in visited):
            edge_color_map.append(QUERY_COLOR)
        else:
            edge_color_map.append(NODE_COLOR)

    pos = nx.get_node_attributes(Graph, 'pos')
    labels = {}
    for edge in Graph.nodes():
        labels[edge] = "edge[" + f"({edge[1].origin.x}, {edge[1].origin.y})" + f"({edge[1].destination.x}," \
            f" {edge[1].destination.y})" + "]"

    options = {
        'node_size': 400,
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 20,
        'with_labels': True,
        'node_color': node_color_map,
        'edge_color': edge_color_map,
        'labels': labels,
        'font_weight': 'bold',
        'font_color': 'black',
        'font_size': 15,
        'connectionstyle': 'bar, fraction = 0',
        'verticalalignment': 'bottom'
    }
    nx.draw(Graph, pos, **options)
    plt.xlim(plt.xlim()[0] - 0.5, plt.xlim()[1] + 0.5)  # Add margin to make sure binary search tree is fully visible
    plt.show()


# Helper method for iterating over binary search tree
def __walk_tree_edges(g, n, prev_x, level):
    level = level + 1
    if n.left is not None:
        min_x = prev_x - 1
        g.add_node(n.left.edge, pos=(min_x, -level))
        g.add_edge(n.edge, n.left.edge)
        __walk_tree_edges(g, n.left, min_x, level)

    if n.right is not None:
        max_x = prev_x + 1
        g.add_node(n.right.edge, pos=(max_x, -level))
        g.add_edge(n.edge, n.right.edge)
        __walk_tree_edges(g, n.right, max_x, level)


def plot_search_structure(search_structure, visited=None):
    Graph = nx.DiGraph(directed=True)
    node = search_structure.root_node
    Graph.add_node(node, pos=(0, 0))
    __walk_searchstructure(Graph, node, 0, 0)

    node_color_map = []
    for node in Graph:
        if visited is not None and any(v.slab == node for v in visited):
            node_color_map.append(QUERY_COLOR)
        else:
            node_color_map.append(NODE_COLOR)

    edge_color_map = []
    for e in Graph.edges():
        # edge is mapped to QUERY_COLOR color if both of it's endpoints are visited
        if visited is not None and any(v.slab == e[0] for v in visited) and any(v.slab == e[1] for v in visited):
            edge_color_map.append(QUERY_COLOR)
        else:
            edge_color_map.append(NODE_COLOR)

    pos = nx.get_node_attributes(Graph, 'pos')
    labels = {}
    for node in Graph.nodes():
        if node.__class__.__name__ == "EndpointNode":
            labels[node] = "E (" + str(node.endpoint.x) + ", " + str(node.endpoint.y) + ")"
        elif node.__class__.__name__ == "SegmentNode":
            labels[node] = "S " + str(node.segment.origin.x) + ", " + str(node.segment.origin.y) + " - " + \
                           str(node.segment.destination.x) + ", " + str(node.segment.destination.y)
        elif node.__class__.__name__ == "TrapezoidNode":
            labels[node] = "T l " + str(node.trapezoid.leftp.x) + ", " + str(node.trapezoid.leftp.y) + " - r " \
                           + str(node.trapezoid.rightp.x) + ", " + str(node.trapezoid.rightp.y)
        else:
            labels[node] = node.__class__.__name__

    # for node in Graph.nodes():
    #     labels[node] = node.__class__.__name__
    options = {
        'node_size': 400,
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 20,
        'with_labels': True,
        'node_color': node_color_map,
        'edge_color': edge_color_map,
        'labels': labels,
        'font_weight': 'bold',
        'font_color': 'black',
        'font_size': 15,
        'connectionstyle': 'bar, fraction = 0',
        'verticalalignment': 'bottom'
    }
    nx.draw(Graph, pos, **options)
    plt.xlim(plt.xlim()[0] - 0.5, plt.xlim()[1] + 0.5)  # Add margin to make sure binary search tree is fully visible
    plt.show()


# Helper method for iterating over the search tree
def __walk_searchstructure(g, n, prev_x, level):
    level = level + 1
    if n.left_child is not None:
        min_x = prev_x - 1
        g.add_node(n.left_child, pos=(min_x, -level))
        g.add_edge(n, n.left_child)
        __walk_searchstructure(g, n.left_child, min_x, level)

    if n.right_child is not None:
        max_x = prev_x + 1
        g.add_node(n.right_child, pos=(max_x, -level))
        g.add_edge(n, n.right_child)
        __walk_searchstructure(g, n.right_child, max_x, level)

# def plot_interactive_graph(dcel):
#     Graph = __draw_graph(dcel)
#     nt = Network("500px", "500px")
#     nt.from_nx(Graph)
#     nt.show("nx.html")
