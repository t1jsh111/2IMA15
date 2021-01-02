import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random as r

NODE_COLOR = 'steelblue'
QUERY_COLOR = 'red'
QUERY_NAME = 'query'

def __draw_graph(dcel):
    Graph = nx.DiGraph(directed=True)
    #pos = []
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


def plot_search_structure(search_structure, visited=None):
    Graph = nx.DiGraph(directed=True)
    node = search_structure.root_node
    Graph.add_node(node, pos=(0,0))
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
        labels[node] = node.__class__.__name__
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