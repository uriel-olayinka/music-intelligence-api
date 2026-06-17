from fastapi import FastAPI, HTTPException
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
    items = results["tracks"]["items"]

    if not items:
        raise HTTPException(status_code=404, detail=f"No track found matching '{track_name}'")

    track = items[0]
    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
        "spotify_id": track["id"],
        "spotify_url": track["external_urls"]["spotify"]
    }

@app.get("/artist/{artist_name}")
def search_artist(artist_name: str):
    results = sp.search(q=artist_name, limit=1, type="artist")
    items = results["artists"]["items"]

    if not items:
        raise HTTPException(404, detail=f"No artist found matching '{artist_name}'")

    artist = items[0]
    return {
        "name": artist["name"],
        "spotify_id": artist["id"],
        "spotify_url": artist["external_urls"]["spotify"],
        "image_url": artist["images"][0]["url"] if artist["images"] else None
    }