from API import SpotifyAPI
import requests
import networkx as nx


def batch(nodes : list, batch_size : int) -> list :
    '''nodes : list of all track object IDs from a network
    batch_size() : Size of each batch, maxsize = 50 
    '''
    batches = []
    batch_size = batch_size if batch_size < 50 else 50      #force size to 50
    for i in range(0, len(nodes), batch_size) :
        batches.append(','.join(nodes[i : i + batch_size]))
    return batches

def node_batch(G : nx.graph, batch_size : int) -> list :
    '''Takes a graph as input, extracts object ID from URIs and creates batches
    to be used for batch API query. Batches are comma separated object IDs
    G : graph -> Input graph
    '''
    nodeList = []
    for node in G.nodes(data = False) :
        nodeList.append(node.split(":")[-1])
        
    trackBatch = batch(nodeList, batch_size)
    
    return trackBatch

def get_track_details(batches : list, api_object, token : str) -> dict :
    '''
    Take a batch as input and query the 'tracks' endpoint to get details
    token : str -> Oauth token
    return : dict with details for all tracks in the batch
    '''
    if(len(batches) == 0) :
        return None
    
    details = []
    for batch in batches :
        try:
            query = "ids=" + batch
            data = api_object.get_data(token, 'tracks', query, batch=True)
            details.append(data)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")  # Handle connection errors
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")  # Handle timeout errors
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")  # Handle JSON parsing errors
        except Exception as err:
            print(f"An unexpected error occurred: {err}")  # Handle other unexpected errors

    return details

def update_track_attributes(G : nx.Graph, track_details : dict) -> None :
    track_details_dict = {}
    for details in track_details :
        for track in details['tracks'] :
            new_dict = {
                track["uri"]: {
                    "popularity": track["popularity"],
                    "duration_ms": track["duration_ms"]
                }
            }
            track_details_dict.update(new_dict)
    nx.set_node_attributes(G, track_details_dict)
    return
         

def get_audio_features(batches : list, api_object, token : str) -> dict :
    '''
    Take a batch as input and query the 'tracks' endpoint to get audio features
    token : str -> Oauth token
    return : dict with audio features for all tracks in the batch
    '''
    if(len(batches) == 0) :
        return None
    
    features = []
    for batch in batches :
        try:
            query = "ids=" + batch
            data = api_object.get_data(token, 'audio-features', query, batch=True)
            features.append(data)
        except Exception as err:
            print(f"An unexpected error occurred: {err}")  # Handle other unexpected errors

    return features

def update_audio_attributes(G : nx.Graph, audio_features : dict) -> None :
    audio_features_dict = {}
    # List of keys to include in the value dictionary.
    keys_to_include = ["acousticness", "danceability", "duration_ms", "energy",
                    "instrumentalness", "key", "liveness", "loudness", "mode",
                    "speechiness", "tempo", "time_signature", "valence"]
    for features in audio_features :
        for feature in features['audio_features'] :
            new_dict = {
                feature['uri'] : {key : feature[key] for key in keys_to_include}
            }
            audio_features_dict.update(new_dict)
            
    nx.set_node_attributes(G, audio_features_dict)
    
    return

    