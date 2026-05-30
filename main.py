from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Music API is alive"}

@app.get("/track/{track_name}")
def get_track(track_name: str):
    return {"track": track_name, "status": "not yet implemented"}
