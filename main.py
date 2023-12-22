import os

from flask import escape
import functions_framework
import yaml
from pathlib import Path
import random
from database import MongoDBConnection
import requests


# Set up MongoDB connection
connection_string = os.environ.get("_DB_STRING")
mongo_database = os.environ.get("_DB_NAME")
spotify_client_id = os.environ.get("_SPOTIFY_CLIENT_ID")
spotify_secret = os.environ.get("_SPOTIFY_SECRET")

# Local development
path = Path(__file__).parent / "./.env.yaml"
environment = os.environ.get("ENV")
if environment == "dev":
    with path.open() as file:
        local_env = yaml.safe_load(file)
        connection_string = local_env.get("_DB_STRING")
        mongo_database = local_env.get("_DB_NAME")
        spotify_client_id = local_env.get("_SPOTIFY_CLIENT_ID")
        spotify_secret = local_env.get("_SPOTIFY_SECRET")

# Create an instance of MongoDBConnection
mongo_connection = MongoDBConnection(connection_string, mongo_database)


def refresh_token(refreshToken):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {spotify_secret}"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refreshToken,
        "client_id": spotify_client_id
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"Error in refresh_token: {e}")
        return None

def recently_played(accessToken):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization": f"Bearer {accessToken}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"Error in getting recently_played: {e}")
        return None



@functions_framework.http
def recent_playlist(request):
    try:
        # Connect to MongoDB
        db = mongo_connection.connect()
        if db is not None:
            random_integer = random.randint(1, 100)

            filter_criteria = { 
                "settings": "auth"
            }
            projection = {"access_token": 1, "refresh_token": 1}
             
            #Get token
            get_token_cursor = db.spotify.find(filter_criteria,projection)
            for document in get_token_cursor:
                accessToken = document.get("access_token")
                refreshToken = document.get("refresh_token")

            #Get recently played
            recently_played_result = recently_played(accessToken)
            if recently_played_result:
                #save playlist
                result = db.spotify.update_one(filter_criteria, {
                    '$set': {
                        'recently_played': recently_played_result
                    }
                })
            else:
                print("Failed to get recently played songs")
            

            #Refresh token
            token_refresh_result =  refresh_token(refreshToken)
            if token_refresh_result:
                access_token = token_refresh_result.get('access_token')
                if access_token:
                    #save access token
                    result = db.spotify.update_one(filter_criteria, {
                        '$set': {
                            'access_token': access_token
                        }
                    })

                else:
                    print("Access token not found in the response.")
            else:
                print("Failed to refresh token.")


            # Example: Returning a response
            return f"recent playlist was modified."

    finally:
        # Disconnect from MongoDB after operations
        mongo_connection.disconnect()
