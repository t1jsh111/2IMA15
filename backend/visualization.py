import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random as r


def __draw_graph(dcel):
    Graph = nx.DiGraph(directed=True)
    # pos = []
    # Add vertices and hedges to the graph
    for vertex in list(dcel.vertices_map.values()):
        Graph.add_node(vertex.name, pos=(vertex.x, vertex.y))
        hedges = dcel.hedges_map.get_all_hedges_of_vertex(vertex)
        for hedge in hedges:
            Graph.add_edges_from([(hedge.origin.name, hedge.destination.name)])

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


def plot_graph(dcel):
    __color_faces(dcel)
    __draw_graph(dcel)
    plt.show()


def plot_slab_decomposition(dcel):
    for vertex in list(dcel.vertices_map.values()):
        plt.axvline(x=vertex.x, color='green', linewidth=3)
    __color_faces(dcel)
    __draw_graph(dcel)
    plt.show()


def plot_slab_binary_search_tree(root_node):
    Graph = nx.DiGraph(directed=True)

    node = root_node
    Graph.add_node(node.slab, pos=(0, 0))
    limit = __walk_tree_slab(Graph, node, 0, 0)

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
        'labels': labels,
        'font_weight': 'bold',
        'font_color': 'black',
        'font_size': 15,
        'connectionstyle': 'bar, fraction = 0',
        'verticalalignment': 'bottom'
    }
    nx.draw(Graph, pos, **options)
    plt.xlim(limit[0] - 1, limit[1] + 1)  # Add margin to make sure binary search tree is fully visible
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

    if level == 1:
        return min_x, max_x


def plot_edges_binary_search_tree(root_node):
    Graph = nx.DiGraph(directed=True)

    node = root_node
    Graph.add_node(node.edge, pos=(0, 0))
    limit = __walk_tree_edges(Graph, node, 0, 0)
    print(limit)

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
        'labels': labels,
        'font_weight': 'bold',
        'font_color': 'black',
        'font_size': 15,
        'connectionstyle': 'bar, fraction = 0',
        'verticalalignment': 'bottom'
    }
    nx.draw(Graph, pos, **options)
    plt.xlim(limit[0]-1, limit[1]+1)  # Add margin to make sure binary search tree is fully visible
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

    if level == 1:
        return min_x, max_x

# def plot_interactive_graph(dcel):
#     Graph = __draw_graph(dcel)
#     nt = Network("500px", "500px")
#     nt.from_nx(Graph)
#     nt.show("nx.html")
