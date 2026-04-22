from fastapi import FastAPI, HTTPException
from . import crud
from .database import init_db
from .schemas import TrackCreate, TrackUpdate, TrackPatch, TrackResponse

app = FastAPI(
    title="Music Service API",
    description="REST API для управления музыкальными треками.",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "FastAPI backend для музыкального сервиса работает"}

@app.get("/tracks", response_model=list[TrackResponse], tags=["Tracks"])
def read_tracks():
    return crud.get_all_tracks()

@app.get("/tracks/{track_id}", response_model=TrackResponse, tags=["Tracks"])
def read_track(track_id: int):
    track = crud.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return track

@app.post("/tracks", response_model=TrackResponse, status_code=201, tags=["Tracks"])
def create_track(track: TrackCreate):
    return crud.create_track(track.model_dump())

@app.put("/tracks/{track_id}", response_model=TrackResponse, tags=["Tracks"])
def update_track(track_id: int, track: TrackUpdate):
    updated = crud.update_track(track_id, track.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return updated

@app.patch("/tracks/{track_id}", response_model=TrackResponse, tags=["Tracks"])
def patch_track(track_id: int, track: TrackPatch):
    updated = crud.patch_track(track_id, track.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return updated

@app.delete("/tracks/{track_id}", tags=["Tracks"])
def delete_track(track_id: int):
    deleted = crud.delete_track(track_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Трек не найден")
    return {"message": "Трек успешно удалён"}