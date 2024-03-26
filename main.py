# %%
import sys 
sys.dont_write_bytecode = True

import json
import networkx as nx
import pandas as pd
from API import SpotifyAPI
from NetworkAnalysis import NetworkAnalysis
import enrich
from graphWalk import graphWalk
import context_recommendation


# %%
spotify = SpotifyAPI()
token = spotify.get_token()
print(f"Token: {token}")

# %%
# spotifyNetwork = NetworkAnalysis(r".\Big Dataset\bigger_graph.pickle", r".\Big Dataset\song_data_bigger.csv")
spotifyNetwork = NetworkAnalysis(r".\Small Dataset\small_graph.pickle", r".\Small Dataset\song_data_smaller.csv")
louvain_communities = spotifyNetwork.get_louvain(resolution=1)
spotifyNetwork.get_connected_components()
# %%
spotifyNetwork.plot_centrality_measures()
# eccentricity = small_graph.eccentricity()
# small_graph.pageRank(alpha=0.85, tol=1e-4, max_iter=500)
print("Start API")
# %%
# Enrich track nodes with API
#Split the nodes into batches for faster querying rather than querying each URI
nodeBatches = enrich.node_batch(spotifyNetwork.G, 50, type = "tracks")

#Get track details and update node attributes
track_details = enrich.get_track_details(nodeBatches, spotify, token)
enrich.update_track_attributes(spotifyNetwork.G, track_details)

# %%
#Get track audio features and update node attributes
audio_features = enrich.get_audio_features(nodeBatches, spotify, token)
enrich.update_audio_attributes(spotifyNetwork.G, audio_features)

# %%
# Get track  and update node attributes
artistBatches = enrich.node_batch(spotifyNetwork.G, 50, type = "artists")
artist_details = enrich.get_artist_details(artistBatches, spotify, token)

all_genres = enrich.get_all_genres(artist_details)
top_genres = top_20_keys = {key : value for key, value in sorted(all_genres.items(), key=lambda item: item[1], reverse=True)[:20]}
enrich.update_artist_details(spotifyNetwork.G, artist_details, list(top_genres))

# %%
# spotifyNetwork.display_nodes()
# # spotifyNetwork.save_graph()
# df = spotifyNetwork.to_dataframe()
# print(df)

# %%
attributes = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'artist_popularity']
recommendations = graphWalk(spotifyNetwork.G, "spotify:track:7o2CTH4ctstm8TNelqjb51", walk_length=20, context=True, attributes=attributes)
print(f"Length : {len(recommendations)}")
for node, attr in recommendations.items() :
    print(f"Track : {node}")
    print(f"Attrs : {attr}")
    
# %%
# import context_recommendation
# attributes = ['popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'artist_popularity']
# sim = context_recommendation.cosine_sim(spotifyNetwork.G, 'spotify:track:55OdqrG8WLmsYyY1jijD9b', 'spotify:track:4w7yrP4RAeeyhfG9nJqQvS', attributes=attributes)
# print(f"Sim : {sim}")

# %%
