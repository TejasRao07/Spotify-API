from dotenv import load_dotenv
import os
import base64
import requests
import json

class SpotifyAPI:
    def __init__(self):
        load_dotenv()                                               # Load environment variables from .env file
        self.tokenURL = "https://accounts.spotify.com/api/token"    # Token auth endpoint
        self.clientID = os.getenv("clientID")                       # client ID of spotify dev account
        self.clientSecret = os.getenv("clientSecret")               # client secret key of spotify dev account
        self.base_URL = "https://api.spotify.com/v1/"               # Data query base URL /artists or /playlist for actual endpoint 
        
    def get_token(self) -> str:
        '''Authenticate user with client ID and key to obtain the Oauth token'''
        authString = f"{self.clientID}:{self.clientSecret}"
        authBytes = authString.encode("utf-8")
        authBase64 = str(base64.b64encode(authBytes), "utf-8")
        headers = {
            "Authorization": "Basic " + authBase64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(url=self.tokenURL, headers=headers, data=data)
        json_result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Expires in: {json_result['expires_in']} secs")
        
        return json_result["access_token"]
    
    def generate_auth_header(self, token: str) -> dict:
        '''Function to generate header with auth token'''
        return {"Authorization": "Bearer " + token}
    
    def get_data(self, token: str, search_type: str, search_param: str = None) -> dict:
         '''token : str -> auth token
        search_type : str -> object type from [artists, tracks, albums, genres, categories]
        search_param : str -> object ID/URI 
        '''
        query_URL = self.base_URL + search_type + '/' + search_param
        headers = self.generate_auth_header(token)
        
        response = requests.get(url=query_URL, headers=headers)
        json_result = response.json()
        print(f"Status Code: {response.status_code}")
        
        return json_result

# example usage
spotify = SpotifyAPI()
token = spotify.get_token()
print(f"Token: {token}")
result = spotify.get_data(token, "tracks", "4cxMGhkinTocPSVVKWIw0d")
print(result)
