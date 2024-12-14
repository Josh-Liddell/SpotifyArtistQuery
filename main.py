import requests
from dotenv import load_dotenv
import os
import base64
from requests import post,get 
import json
import pandas as pd

load_dotenv()

client_id = os.getenv ("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}



def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    with open("token_data.json", "w") as file:
        json.dump(json_result, file, indent=4)
    return json_result


token = get_token()
df = pd.DataFrame()
while True:
    songNames = []
    ui = input("Search for an artist to get their top 10 songs! (or q to quit or s to save to a csv): ")
    if ui.lower() == "q":
        print("Program ended")
        break
    elif ui.lower() == "s":
        print(df)
        df.to_csv("output.csv")
        break
    if len(ui) > 0:
        result = search_for_artist(token, ui)
        print(result["name"])
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)

        for song in songs:
            songNames.append(song['name'])
            print(song['name'])
        df[result["name"]] = songNames





