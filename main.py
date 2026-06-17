from fastapi import FastAPI, HTTPException
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
from database import init_db, SessionLocal
from models import SearchHistory

init_db()

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

    db = SessionLocal()
    history_entry = SearchHistory(
        query_type="track",
        query_value=track_name,
        result_name=track["name"],
        spotify_id=track["id"]
    )
    db.add(history_entry)
    db.commit()
    db.close()

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

    db = SessionLocal()
    history_entry = SearchHistory(
        query_type="artist",
        query_value=artist_name,
        result_name=artist["name"],
        spotify_id=artist["id"]
    )
    db.add(history_entry)
    db.commit()
    db.close()

    return {
        "name": artist["name"],
        "spotify_id": artist["id"],
        "spotify_url": artist["external_urls"]["spotify"],
        "image_url": artist["images"][0]["url"] if artist["images"] else None
    }

@app.get("/history")
def get_history():
    db = SessionLocal()
    entries = db.query(SearchHistory).order_by(SearchHistory.searched_at.desc()).limit(20).all()
    db.close()

    return [
        {
            "query_type": e.query_type,
            "query_value": e.query_value,
            "result_name": e.result_name,
            "spotify_id": e.spotify_id,
            "searched_at": e.searched_at
        }
        for e in entries
    ]