# %%
import pickle
import matplotlib.pyplot as plt
import networkx as nx

with open(r".\Small Dataset\small_graph.pickle", 'rb') as f :
    data = pickle.load(f)

# %%

nx.draw_networkx(data, with_labels=False)
for node, attrs in data.nodes(data=True):
    for attr, value in attrs.items():
        if isinstance(value, list):
            print(data.nodes[node][attr])
            data.nodes[node][attr] = str(value)

for u, v, attrs in data.edges(data=True):
    for attr, value in attrs.items():
        if isinstance(value, list):
            data[u][v][attr] = str(value)
# %%
nx.write_gexf(data, "smallGraph.gexf")
nx.write_graphml(data, "smallGraph.graphml")
# %%
