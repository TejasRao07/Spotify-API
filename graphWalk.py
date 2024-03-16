import networkx as nx
import random

'''Function for the graph walk, takes a song as input and performs a graph walk based on the
edge weights of neighboring nodes as a simple recommendation system '''

def getRecommendation(G : nx.graph, current_track : nx.nodes, prev_tracks : list) -> nx.nodes :
    '''Gets next recommendation given a current track. Iterates through all neighbours and randomly selects one out of the neighbours with
    highest edge weight
    G : nx.graph -> networkX graph
    current_track : nx.node -> current track node
    returns : Node of next track '''
    
    neighbours = list(G.neighbors(current_track))
    # print(f"neighbours : {neighbours}")
    if not neighbours :
        return None
    
    maxEdgeweight = -1
    candidates = []
    for neighbour in neighbours :
        if(neighbour in prev_tracks) :
            continue
        edgeWeight = G[current_track][neighbour]["weight"]
        if(edgeWeight > maxEdgeweight) :
            maxEdgeweight = edgeWeight
            candidates = [neighbour]
        elif(edgeWeight == maxEdgeweight) :
            candidates.append(neighbour)
    

    return random.choice(candidates) if candidates else None
    
def graphWalk(G : nx.Graph, current_track : nx.nodes, walk_length : int = 10) -> list :
    '''Take a graph and a starting track and return a list of recommendations from starting track
    G : networkX graph -> co-occurence graph
    current_track : networkX node -> starting track
    walk_length : int -> number of recommendations required/ size of graph walk
    
    returns : list of recommended track nodes'''
    recommendations = {}
    recommendations[current_track] = G.nodes[current_track]
    played_tracks = []
    for _ in range(walk_length) :
        print(f"Current Track : {current_track}")
        if(current_track == None) :
            break 
        next_track = getRecommendation(G, current_track, played_tracks)
        if(next_track == None) :
            next_track = random.choice(G.nodes())
        
        played_tracks.append(next_track)
        if(len(played_tracks) > walk_length) :
            played_tracks.pop(0)
            
        recommendations[next_track] = G.nodes[next_track]
        current_track = next_track
    
    return recommendations
    
 
