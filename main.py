from fastapi import FastAPI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
))

@app.get("/")
def root():
    return {"message": "Music API is alive"}

@app.get("/track/{track_name}")
def search_track(track_name: str):
    results = sp.search(q=track_name, limit=1, type="track")
    track = results["tracks"]["items"][0]
    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
        "spotify_id": track["id"],
        "spotify_url": track["external_urls"]["spotify"]
    }
