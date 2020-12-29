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


def plot_binary_search_tree(root_node):
    Graph = nx.DiGraph(directed=True)

    node = root_node
    Graph.add_node(node.slab, pos=(0, 0))
    __walk_tree(Graph, node, 0, 0)

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
    plt.show()


# Helper method for iterating over binary search tree
def __walk_tree(g, n, prev_x, level):
    level = level + 1
    if n.left is not None:
        g.add_node(n.left.slab, pos=(prev_x - 1, -level))
        g.add_edge(n.slab, n.left.slab)
        __walk_tree(g, n.left, prev_x - 1, level)

    if n.right is not None:
        g.add_node(n.right.slab, pos=(prev_x + 1, -level))
        g.add_edge(n.slab, n.right.slab)
        __walk_tree(g, n.right, prev_x + 1, level)

# def plot_interactive_graph(dcel):
#     Graph = __draw_graph(dcel)
#     nt = Network("500px", "500px")
#     nt.from_nx(Graph)
#     nt.show("nx.html")
