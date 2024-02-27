# %%
import pickle
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

# Load smaller graph
with open(r".\Small Dataset\small_graph.pickle", 'rb') as f :
    G = pickle.load(f)

# Reading the song G file to enrich network nodes with song name.
# Node names are the song URI which is not easily readable
song_G = pd.read_csv(r".\Small Dataset\song_data_smaller.csv")
song_name_dict = dict(zip(song_G["song_id"], song_G["song_name"]))
artist_name_dict = dict(zip(song_G["song_id"], song_G["artist_name"]))
album_name_dict = dict(zip(song_G["song_id"], song_G["album_name"]))

nx.set_node_attributes(G, song_name_dict, "Track Name")
nx.set_node_attributes(G, artist_name_dict, "Artist Name")
nx.set_node_attributes(G, album_name_dict, "Album Name")

# %%
#print out attributes of each node
labels = nx.get_node_attributes(G, 'Track Name')
nx.draw_networkx(G, with_labels=False, labels = labels)
for node, attrs in G.nodes(data=True):
    for attr, value in attrs.items():
        print(f"attr : {attr} \n val : {G.nodes[node][attr]}")

# %%
# print out attributes of each edge
for u, v, attrs in G.edges(data=True):
    for attr, value in attrs.items():
        print(f"u: {u}, v: {v}, attr: {attr}, val: {G[u][v][attr]}")
        if isinstance(value, list):
            G[u][v][attr] = str(value)
# %% 
# store node attributes in a dict
node_attrs = {}
for node, attrs in G.nodes(data = True) :
    for attr, value in attrs.items() :
        print(f"attr : {attr} | val : {value}")
print(node_attrs)           

# %%
# Write networkX graph into a gephi readable file format - gexf/ graphML
nx.write_gexf(G, "smallGraph.gexf")
nx.write_graphml(G, "smallGraph.graphml")


# %%
# Get connected components in the network
CCs = list(nx.connected_components(G))
print(f"Number of CCs : {len(CCs)}")
for i, cc in enumerate(CCs) :
    print(f"CC {i} : {cc}")
    
    
# %%
#Get k-core metrics
k_values = range(3, 100)
data = [] 
for k in k_values :
    k_core = nx.k_core(G, k = k)
    data.append(k_core.number_of_nodes())

plt.plot(k_values, data)
plt.xlabel("k")
plt.ylabel("No. Of Nodes in k-core")
plt.grid()
plt.show()

# %%
# Freeman's centrality measures
degree_centrality = list(nx.degree_centrality(G).values())
betweenness_centrality = list(nx.betweenness_centrality(G).values())
closeness_centrality = list(nx.closeness_centrality(G).values())
eigenvector_centrality = list(nx.eigenvector_centrality(G).values())

# Creating histograms for each centrality measure
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Degree Centrality Histogram
axs[0, 0].hist(degree_centrality, bins=100, color='skyblue')
axs[0, 0].set_title('Degree Centrality')
axs[0, 0].set_xlabel("Values")
axs[0, 0].set_ylabel("Count of Nodes")

# Betweenness Centrality Histogram
axs[0, 1].hist(betweenness_centrality, bins=100, color='lightgreen')
axs[0, 1].set_title('Betweenness Centrality')
axs[0, 1].set_xlabel("Values")
axs[0, 1].set_ylabel("Count of Nodes")

# Closeness Centrality Histogram
axs[1, 0].hist(closeness_centrality, bins=100, color='lightcoral')
axs[1, 0].set_title('Closeness Centrality')
axs[1, 0].set_xlabel("Values")
axs[1, 0].set_ylabel("Count of Nodes")

# Eigenvector Centrality Histogram
axs[1, 1].hist(eigenvector_centrality, bins=100, color='wheat')
axs[1, 1].set_title('Eigenvector Centrality')
axs[1, 1].set_xlabel("Values")
axs[1, 1].set_ylabel("Count of Nodes")

plt.tight_layout()
plt.show()
# %%
