import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def __draw_graph__(dcel):
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
        'font_size': 15
    }
    nx.draw(Graph, pos, **options)
    # plt.axvline(x=2)
    # plt.scatter(2, 5, marker=".", s=200)


def plot_graph(dcel):
    __draw_graph__(dcel)
    plt.show()


def plot_slab_decomposition(dcel):
    __draw_graph__(dcel)
    for vertex in list(dcel.vertices_map.values()):
        plt.axvline(x=vertex.x, color='green', linewidth=3)
    plt.show()