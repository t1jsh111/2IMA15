import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random as r


def __draw_graph(dcel):
    Graph = nx.DiGraph(directed=True)
    # Add vertices and hedges to the graph
    for vertex in list(dcel.vertices_map.values()):
        Graph.add_node(vertex.name, pos=(vertex.x, vertex.y))
        hedges = dcel.hedges_map.get_all_hedges_of_vertex(vertex)
        for hedge in hedges:
            Graph.add_edges_from([(hedge.origin.name, hedge.destination.name)])

    pos = nx.get_node_attributes(Graph, 'pos')
    options = {
        'node_size': 1500,
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 16,
        'with_labels': True,
        'labels': pos,
        'font_weight': 'bold',
        'font_color': 'orange',
        'font_size': 15,
        'connectionstyle': 'arc3, rad = 0.04'
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

            polygon = plt.Polygon(vertex_list, color=[r.random(), r.random(), r.random()], alpha=0.5)
            plt.gca().add_patch(polygon)


def plot_graph(dcel):
    __draw_graph(dcel)
    __color_faces(dcel)
    plt.show()


def plot_slab_decomposition(dcel):
    __draw_graph(dcel)
    for vertex in list(dcel.vertices_map.values()):
        plt.axvline(x=vertex.x, color='green', linewidth=3)
    plt.show()

# def plot_interactive_graph(dcel):
#     Graph = __draw_graph(dcel)
#     nt = Network("500px", "500px")
#     nt.from_nx(Graph)
#     nt.show("nx.html")