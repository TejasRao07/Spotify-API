# %%
import pickle
import matplotlib.pyplot as plt
import networkx as nx
import community
import pandas as pd
import numpy as np
from networkx.algorithms.community import girvan_newman


class NetworkAnalysis : 
    def __init__(self, pickle_file, song_data) -> None:
        # Load graph
        with open(pickle_file, 'rb') as f :
            self.G = pickle.load(f)
            
        # Reading the song G file to enrich network nodes with song name.
        # Node names are the song URI which is not easily readable
        song_data = pd.read_csv(song_data)
        song_name_dict = dict(zip(song_data["song_id"], song_data["song_name"]))
        artist_name_dict = dict(zip(song_data["song_id"], song_data["artist_name"]))
        album_name_dict = dict(zip(song_data["song_id"], song_data["album_name"]))
        artist_URI_dict = dict(zip(song_data["song_id"], song_data["artist_uri"]))
        album_URI_dict = dict(zip(song_data["song_id"], song_data["album_uri"]))

        nx.set_node_attributes(self.G, song_name_dict, "Track Name")
        nx.set_node_attributes(self.G, artist_name_dict, "Artist Name")
        nx.set_node_attributes(self.G, album_name_dict, "Album Name")
        nx.set_node_attributes(self.G, artist_URI_dict, "Artist URI")
        nx.set_node_attributes(self.G, album_URI_dict, "Album URI")

    def display_nodes(self) :
        for node, attrs in self.G.nodes(data = True) :
            print(f"Node : {node}\nattrs : {attrs}")
    
    def diameter(self) -> int :
        return nx.diameter(self.G)
    
    def avgDegree(self) -> int :
        # Calculate the average degree
        return sum(dict(self.G.degree()).values()) / self.G.number_of_nodes()
    
    def avg_path_length(self) -> float :
        return nx.average_shortest_path_length(self.G) 
    
    def avgClusteringCoefficient(self) -> float:
        return nx.average_clustering(self.G)
    
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
        # Convert all node attributes to strings
        for node, attrs in self.G.nodes(data=True):
            for attr, value in attrs.items():
                # Convert each attribute value to string
                if(isinstance(value, list)) :
                    self.G.nodes[node][attr] = str(value)

        # Convert all edge attributes to strings
        for u, v, attrs in self.G.edges(data=True):
            for attr, value in attrs.items():
                # Convert each attribute value to string
                if(isinstance(value, list)) :
                    self.G[u][v][attr] = str(value)
        nx.write_gexf(self.G, "smallGraph.gexf")
        nx.write_graphml(self.G, "smallGraph.graphml")
    
    def get_connected_components(self) -> None :
        # Get connected components in the network
        CCs = list(nx.connected_components(self.G))
        print(f"Number of CCs : {len(CCs)}")
    
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
            degree_centrality = nx.degree_centrality(self.G)
            nx.set_node_attributes(self.G, degree_centrality, "Degree Centrality")
            
            betweenness_centrality = nx.betweenness_centrality(self.G)
            nx.set_node_attributes(self.G, betweenness_centrality, "Betweenness Centrality")
            
            closeness_centrality = nx.closeness_centrality(self.G)
            nx.set_node_attributes(self.G, closeness_centrality, "Closeness Centrality")
            
            eigenvector_centrality = nx.eigenvector_centrality(self.G)
            nx.set_node_attributes(self.G, eigenvector_centrality, "Eigenvector Centrality")

            fig, axs = plt.subplots(2, 2, figsize=(14, 10))
            self._plot_histogram(axs[0, 0], list(degree_centrality.values()), 'Degree Centrality', 'skyblue')
            self._plot_histogram(axs[0, 1], list(betweenness_centrality.values()), 'Betweenness Centrality', 'lightgreen')
            self._plot_histogram(axs[1, 0], list(closeness_centrality.values()), 'Closeness Centrality', 'lightcoral')
            self._plot_histogram(axs[1, 1], list(eigenvector_centrality.values()), 'Eigenvector Centrality', 'wheat')
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
    
    def eccentricity(self) :
        '''
        Calculate eccentricity and update it as a node attribute
        '''
        eccentricity = nx.eccentricity(self.G)
        nx.set_node_attributes(self.G, eccentricity, "Eccentricity")
        return eccentricity
    
    def pageRank(self, alpha : float = 0.85, tol : float = 1e-3, max_iter : int = 100) :
        '''Calculate pagerank for all nodes in the network
        alpha : float -> damping paramter, default = 0.85
        tol : float -> Error tolerance used to check convergence in power method solver.
        max_iter : int -> Maximum number of iterations in power method eigenvalue solver.
        '''
        pageRank = nx.pagerank(self.G, alpha=alpha, tol=tol, max_iter=max_iter)
        nx.set_node_attributes(self.G, pageRank, "PageRank")
        
    def girvan_newman(self, num_communities = 10) -> list :
        """
        Implement the Girvan-Newman algorithm for community detection.
        
        Parameters:
        - G: A NetworkX graph.
        - num_communities: Desired number of communities. The algorithm stops when this number is reached.
        
        Returns:
        - A list of sets, where each set contains the nodes in one community.
        """
        G_copy = self.G.copy()
        communities = []
        while(len(communities) < num_communities) :
            edge_betweeness = nx.edge_betweenness_centrality(G_copy)
            max_edge = max(edge_betweeness, key=edge_betweeness.get)
            G_copy.remove_edge(*max_edge)
            
            communities = [list(c) for c in nx.connected_components(G_copy)]
            
            if(G_copy.number_of_edges() == 0 ) :
                break
        
        return communities
    
    def get_louvain(self, resolution = 1) -> list :
        """
        Implement the Girvan-Newman algorithm for community detection.
        
        Parameters:
        - G: A NetworkX graph.
        - resolution: Desired number of communities. Increase for fewer and decrease for more communities
        
        Returns:
        - A list of sets, where each set contains the nodes in one community.
        """
        communities_dict = {}
        louvain_communities = nx.community.louvain_communities(self.G, resolution=resolution)
        for index, item in enumerate(louvain_communities) :
            for track in item :
                newDict = {track : index}
                communities_dict.update(newDict)
                
        nx.set_node_attributes(self.G, communities_dict, "Modularity")
        
        return nx.community.louvain_communities(self.G, resolution=resolution)

# %%
# spotify = NetworkAnalysis(r".\Small Dataset\small_graph.pickle", r".\Small Dataset\song_data_smaller.csv" )
# comms = spotify.get_louvain(resolution=1)
# print(f"comms : {comms}")
# spotify.draw_network()
# spotify.display_nodes()
# %%