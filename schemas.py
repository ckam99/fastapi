from pydantic import BaseModel
from typing import List, Optional


class Tournament(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True


class TournamentIn(BaseModel):
    name: str


class Team(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True


class TeamIn(BaseModel):
    name: str


class Event(BaseModel):
    id: int
    name: Optional[str]
    tournament: Tournament = None
    participants: List[Team] = []

    class Config:
        orm_mode = True


class EventIn(BaseModel):
    name: str
    tournament: int
    participants: List[int] = []
