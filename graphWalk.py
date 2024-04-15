import networkx as nx
import random
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

'''Function for the graph walk, takes a song as input and performs a graph walk based on the
edge weights of neighboring nodes as a simple recommendation system '''


def cosine_sim(G : nx.graph, u : nx.nodes, v : nx.nodes, attributes : list) -> float :
    '''Gets next recommendation given a current track. Iterates through all neighbours and selects the one with highest cosine similarity based 
    based on the attributes selected
    @params
    G : nx.graph -> networkX graph
    u : nx.node -> current track node
    v : nx.node -> neighbouring track node
    attributes : list -> List of attributes to check cosine similarity on 

    returns : Float -> Cosine similarity of nodes u and v'''
    
    attributes_1 = G.nodes[u]
    attributes_2 = G.nodes[v]
    
    vec1 = []
    for k, v in attributes_1.items() :
        if(k in attributes) :
            vec1.append(v)
            
    vec2 = []
    for k, v in attributes_2.items() :
        if(k in attributes) :
            vec2.append(v)
    
    vec1 = np.array(vec1).reshape(1, -1)
    vec2 = np.array(vec2).reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def jaccard_similarity(list1 : list, list2 : list) -> float:
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    print(f"intersection : {intersection}")
    print(f"union : {union}")
    return intersection / union


def getRecommendation(G : nx.graph, current_track : nx.nodes, prev_tracks : list, teleport : float = 0.1, context : str = False, attributes : list = ['popularity']) -> nx.nodes :
    '''Gets next recommendation given a current track. Iterates through all neighbours and randomly selects one out of the neighbours with
    highest edge weight
    @params
    G : nx.graph -> networkX graph
    current_track : nx.node -> current track node
    prev_tracks : list(nx.nodes) -> cache of recommended songs so far to avoid short cycles of recommendations
    teleport : float(0, 1) -> teleportation probability. Probability of abandoning current walk and teleporting to a new node for a new walk.
    
    returns : Node of next track '''
    
    if(random.random() <= teleport) :
        all_nodes = list(set(G.nodes) - set(prev_tracks))
        print(f"Teleported")
        return random.choice(all_nodes)
    
    neighbours = list(G.neighbors(current_track))
    # print(f"neighbours : {neighbours}")
    if not neighbours :
        return None
    
    maxEdgeweight = -1
    maxSimilarity = -1
    candidates = []
    for neighbour in neighbours :
        if(neighbour in prev_tracks) :
            continue
        if(context) :
            similarity = cosine_sim(G, current_track, neighbour, attributes = attributes)
            if(similarity > maxSimilarity) :
                maxSimilarity = similarity
                candidates = [neighbour]
            elif(similarity == maxSimilarity) :
                candidates.append(neighbour)
            
        else :
            edgeWeight = G[current_track][neighbour]["weight"]
            if(edgeWeight > maxEdgeweight) :
                maxEdgeweight = edgeWeight
                candidates = [neighbour]
            elif(edgeWeight == maxEdgeweight) :
                candidates.append(neighbour)
    
    if(len(candidates)) :
        print(f"u : {current_track} | v : {candidates[0]} | Cos similarity : {maxSimilarity}")

    return random.choice(candidates) if candidates else None



    
def graphWalk(G : nx.Graph, current_track : nx.nodes, walk_length : int = 10, teleport : float = 0.1, context = False, attributes : list = ['popularity']) -> list :
    '''Take a graph and a starting track and return a list of recommendations from starting track
    G : networkX graph -> co-occurence graph
    current_track : networkX node -> starting track
    walk_length : int -> number of recommendations required/ size of graph walk
    teleport : float(0, 1) -> teleportation probability. Probability of abandoning current walk and teleporting to a new node for a new walk.
    
    returns : list of recommended track nodes'''

    recommendations = {}
    recommendations[current_track] = G.nodes[current_track]
    played_tracks = []
    for _ in range(walk_length) :
        # print(f"Current Track : {current_track}")
        if(current_track == None) :
            break 
        next_track = getRecommendation(G, current_track, played_tracks, teleport=teleport, context=context, attributes=attributes)
        if(next_track == None) :
            next_track = random.choice(list(G.nodes()))
        
        played_tracks.append(next_track)
        if(len(played_tracks) > walk_length) :
            played_tracks.pop(0)
            
        recommendations[next_track] = G.nodes[next_track]
        current_track = next_track
    
    return recommendations

 
