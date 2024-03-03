import json
from API import SpotifyAPI
from NetworkAnalysis import NetworkAnalysis
from enrich import *
import networkx as nx

spotify = SpotifyAPI()
token = spotify.get_token()
print(f"Token: {token}")
# result = spotify.get_data(token, "tracks", "4cxMGhkinTocPSVVKWIw0d")
# print(result)

small_graph = NetworkAnalysis(r".\Small Dataset\small_graph.pickle", r".\Small Dataset\song_data_smaller.csv")

# Enrich track nodes with API
#Split the nodes into batches for faster querying rather than querying each URI
nodeBatches = node_batch(small_graph.G, 50)

#Get track details and update node attributes
track_details = get_track_details(nodeBatches, spotify, token)
update_track_attributes(small_graph.G, track_details)

#Get track audio features and update node attributes
audio_features = get_audio_features(nodeBatches, spotify, token)
update_audio_attributes(small_graph.G, audio_features)

small_graph.display_nodes()