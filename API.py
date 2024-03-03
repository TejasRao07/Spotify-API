from dotenv import load_dotenv
import os
import base64
import requests
import json

class SpotifyAPI:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.tokenURL = "https://accounts.spotify.com/api/token"
        self.clientID = os.getenv("clientID")
        self.clientSecret = os.getenv("clientSecret")
        self.base_URL = "https://api.spotify.com/v1/"
        
    def get_token(self) -> str:
        '''POST request to auth server to obtain client token for data requests
        '''
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
        '''Generate a header in the required format for spotify API
        '''
        return {"Authorization": "Bearer " + token}
    
    def get_data(self, token: str, search_type: str, search_param: str = None, batch = False) -> dict:
        '''token : str -> auth token provided by authClient
        search_type : str -> type of resource we are querying - audio-features/tracks/playlists/artists/albums
        search_param : str -> resource URI
        batch : bool -> if true then send bulk request with multiple comma-separated URIs 
        '''
        if(batch) :
            query_URL = self.base_URL + search_type + '?' + search_param
        else :
            query_URL = self.base_URL + search_type + '/' + search_param
        headers = self.generate_auth_header(token)
        
        response = requests.get(url=query_URL, headers=headers)
        json_result = response.json()
        # print(f"Status Code: {response.status_code}")
        
        return json_result

