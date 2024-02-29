# %%
import pickle
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

class NetworkAnalysis : 
    def __init__(self, pickle_file, song_data) -> None:
        # Load smaller graph
        with open(r".\Small Dataset\small_graph.pickle", 'rb') as f :
            self.G = pickle.load(f)
            
        # Reading the song G file to enrich network nodes with song name.
        # Node names are the song URI which is not easily readable
        song_data = pd.read_csv(r".\Small Dataset\song_data_smaller.csv")
        song_name_dict = dict(zip(song_data["song_id"], song_data["song_name"]))
        artist_name_dict = dict(zip(song_data["song_id"], song_data["artist_name"]))
        album_name_dict = dict(zip(song_data["song_id"], song_data["album_name"]))

        nx.set_node_attributes(self.G, song_name_dict, "Track Name")
        nx.set_node_attributes(self.G, artist_name_dict, "Artist Name")
        nx.set_node_attributes(self.G, album_name_dict, "Album Name")

    def diameter(self) -> int :
        return nx.diameter(G)
    
    def avgDegree(self) -> int :
        # Calculate the average degree
        return sum(dict(self.G.degree()).values()) / self.G.number_of_nodes()
    
    def avg_path_length(self) -> float :
        return nx.average_shortest_path_length(G) 
    
    def avgClusteringCoefficient(self) -> float:
        return nx.average_clustering(G)
    
    def draw_network(self) -> None : 
        #print out attributes of each node
        labels = nx.get_node_attributes(self.G, 'Track Name')
        nx.draw_networkx(self.G, with_labels=False, labels = labels)
        for node, attrs in self.G.nodes(data=True):
            for attr, value in attrs.items():
                print(f"attr : {attr} \n val : {self.G.nodes[node][attr]}")
                
        # print out attributes of each edge
        for u, v, attrs in self.G.edges(data=True):
            for attr, value in attrs.items():
                print(f"u: {u}, v: {v}, attr: {attr}, val: {self.G[u][v][attr]}")
                if isinstance(value, list):
                    self.G[u][v][attr] = str(value)

    def save_graph(self) -> None :
        # Write networkX graph into a gephi readable file format - gexf/ graphML
        nx.write_gexf(self.G, "smallGraph.gexf")
        nx.write_graphml(self.G, "smallGraph.graphml")
    
    def get_connected_components(self) -> None :
        # Get connected components in the network
        CCs = list(nx.connected_components(self.G))
        print(f"Number of CCs : {len(CCs)}")
        for i, cc in enumerate(CCs) :
            print(f"CC {i} : {cc}")
    
    def k_core_analysis(self) -> None :
        #Get k-core metrics
        k_values = range(3, 100)
        data = [] 
        for k in k_values :
            k_core = nx.k_core(self.G, k = k)
            data.append(k_core.number_of_nodes())

        plt.plot(k_values, data)
        plt.xlabel("k")
        plt.ylabel("No. Of Nodes in k-core")
        plt.grid()
        plt.show()

    def plot_centrality_measures(self) -> None:
            """Freeman's centrality measures and creating histograms for each centrality measure."""
            degree_centrality = list(nx.degree_centrality(self.G).values())
            betweenness_centrality = list(nx.betweenness_centrality(self.G).values())
            closeness_centrality = list(nx.closeness_centrality(self.G).values())
            eigenvector_centrality = list(nx.eigenvector_centrality(self.G).values())

            fig, axs = plt.subplots(2, 2, figsize=(14, 10))
            self._plot_histogram(axs[0, 0], degree_centrality, 'Degree Centrality', 'skyblue')
            self._plot_histogram(axs[0, 1], betweenness_centrality, 'Betweenness Centrality', 'lightgreen')
            self._plot_histogram(axs[1, 0], closeness_centrality, 'Closeness Centrality', 'lightcoral')
            self._plot_histogram(axs[1, 1], eigenvector_centrality, 'Eigenvector Centrality', 'wheat')
            plt.tight_layout()
            plt.show()

    def _plot_histogram(self, ax, data, title, color):
            """Helper function to plot histograms for centrality measures."""
            ax.hist(data, bins=100, color=color)
            ax.set_title(title)
            ax.set_xlabel("Values")
            ax.set_ylabel("Count of Nodes")
            
            # Calculate statistics
            mean_val = np.mean(data)
            median_val = np.median(data)
            # For mode, you'd typically find the most frequent value, but it's complicated for continuous data.
            # mode_val = statistics.mode(data) # This might not be applicable for all data sets.

            # Draw lines for mean and median
            ax.axvline(mean_val, color='k', linestyle='dashed', linewidth=1)
            ax.axvline(median_val, color='m', linestyle='dashed', linewidth=1)
            # ax.axvline(mode_val, color='g', linestyle='dashed', linewidth=1) # If you decide to calculate mode

            # Adding text labels for mean and median
            ax.text(mean_val, ax.get_ylim()[1]*0.95, f"Mean: {mean_val:.5f}", ha='right', color='k')
            ax.text(median_val, ax.get_ylim()[1]*0.85, f"Median: {median_val:.5f}", color='m')
            # ax.text(mode_val, ax.get_ylim()[1]*0.75, 'Mode', ha='right', color='g') # If you decide to include mode


# %%
spotify = NetworkAnalysis(r".\Small Dataset\small_graph.pickle", r".\Small Dataset\song_data_smaller.csv" )
spotify.draw_network()
spotify.get_connected_components()
spotify.plot_centrality_measures()
diameter = spotify.diameter()
print(f"Network Diameter : {diameter}")
avgPathLength = spotify.avg_path_length()
print(f"Avg Path Length : {avgPathLength}")
avgClustering = spotify.avgClusteringCoefficient()
print(f"Avg Clustering : {avgClustering}")
# %%
degree_centrality = nx.degree_centrality(spotify.G)
print(degree_centrality)
avg_degree = spotify.avgDegree()
print(f"Avg Degree : {avg_degree}")

# %%
