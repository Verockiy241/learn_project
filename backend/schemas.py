from typing import Optional
from pydantic import BaseModel, Field

class TrackBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Название трека")
    artist: str = Field(..., min_length=1, max_length=100, description="Исполнитель")
    genre: Optional[str] = Field(default=None, max_length=50, description="Жанр")
    bpm: Optional[int] = Field(default=None, gt=0, description="Темп (BPM)")
    duration_sec: Optional[int] = Field(default=None, gt=0, description="Длительность (Сек.)")
    daw: Optional[str] = Field(default=None, max_length=50, description="DAW")
    track_key: Optional[str] = Field(default=None, max_length=10, description="Тональность")

class TrackCreate(TrackBase):
    pass

class TrackUpdate(TrackBase):
    pass

class TrackPatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    artist: Optional[str] = Field(default=None, min_length=1, max_length=100)
    genre: Optional[str] = Field(default=None, max_length=50)
    bpm: Optional[int] = Field(default=None, gt=0)
    duration_sec: Optional[int] = Field(default=None, gt=0)
    daw: Optional[str] = Field(default=None, max_length=50)
    track_key: Optional[str] = Field(default=None, max_length=10)

class TrackResponse(TrackBase):
    id: int