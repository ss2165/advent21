import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
tile = np.genfromtxt("../inputs/day15.txt", delimiter=1, dtype=int)
X, Y = tile.shape

inpar = np.zeros((X*5, Y*5), dtype=int)

for x in range(5):
    for y in range(5):
        newtile = (tile+x+y)%9
        newtile[newtile==0] = 9
        inpar[x*X:(x+1)*X, y*Y:(y+1)*Y] = newtile

X, Y = inpar.shape
G = nx.DiGraph()
for i in range(X):
    for j in range(Y):
        if i != X-1:
            G.add_edge((i, j), (i+1, j), weight=inpar[i+1, j])
            G.add_edge((i+1, j), (i, j), weight=inpar[i, j])
        if j != Y-1:
            G.add_edge((i, j), (i, j+1), weight=inpar[i, j+1])
            G.add_edge((i, j+1), (i, j), weight=inpar[i, j])

def draw(G):
    edge_labels = nx.get_edge_attributes(G,'weight') # key is edge, pls check for your case
    formatted_edge_labels = {(elem[0],elem[1]):edge_labels[elem] for elem in edge_labels}
    pos = nx.spring_layout(G, iterations=100, seed=39775)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels)
    nx.draw(G)
    plt.savefig("del.png")
    # G = nx.grid_2d_graph(X, Y)
    # print(G.edges(data="weight"))

print(single_source_dijkstra(G, (0, 0), (X-1, Y-1))[0])