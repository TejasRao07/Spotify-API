# %%
import sys 
sys.dont_write_bytecode = True

import json
from API import SpotifyAPI
from NetworkAnalysis import NetworkAnalysis
from enrich import *
import networkx as nx


# %%
spotify = SpotifyAPI()
token = spotify.get_token()
print(f"Token: {token}")

# %%
small_graph = NetworkAnalysis(r".\Big Dataset\bigger_graph.pickle", r".\Big Dataset\song_data_bigger.csv")
louvain_communities = small_graph.get_louvain(resolution=1)
small_graph.get_connected_components()
# %%
small_graph.plot_centrality_measures()
eccentricity = small_graph.eccentricity()
small_graph.pageRank(alpha=0.85, tol=1e-4, max_iter=500)
diameter = small_graph.diameter()
# print(f"eccentricity : {eccentricity}")
# print("Start API")
# %%
# Enrich track nodes with API
#Split the nodes into batches for faster querying rather than querying each URI
nodeBatches = node_batch(small_graph.G, 50, type = "tracks")

#Get track details and update node attributes
track_details = get_track_details(nodeBatches, spotify, token)
update_track_attributes(small_graph.G, track_details)

# %%
#Get track audio features and update node attributes
audio_features = get_audio_features(nodeBatches, spotify, token)
update_audio_attributes(small_graph.G, audio_features)

# %%
# Get track  and update node attributes
artistBatches = node_batch(small_graph.G, 50, type = "artists")
artist_details = get_artist_details(artistBatches, spotify, token)

all_genres = get_all_genres(artist_details)
top_genres = top_20_keys = {key : value for key, value in sorted(all_genres.items(), key=lambda item: item[1], reverse=True)[:10]}
update_artist_details(small_graph.G, artist_details, list(top_genres))

# print(f"All Genres : {top_genres}")
# # %%
small_graph.display_nodes()

small_graph.save_graph()
# # %%
 
# %%
