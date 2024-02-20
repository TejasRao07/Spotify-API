import requests
import json

authURL = "https://accounts.spotify.com/api/token"
clientID = "73829530b7f74babafa110d4dd5bf274"
clientSecret = "c25cccf74fa54c579838da61cc581728"

headers = {
    
}

params = {
    
}

r = requests.post(url=authURL, headers=headers, params=params)

def getToken(url : str, clientID : str, clientKey : str) -> str :
    