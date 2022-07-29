import uuid
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "..."
            }
        }


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }


class Metadata(BaseModel):
    data_version: str = Field(...)
    match_id: str = Field(...)
    participants: Optional[List[str]] = Field(...)


class Companion(BaseModel):
    content_ID: str = Field(...)
    skin_ID: int = Field(...)
    species: str = Field(...)


class Participants(BaseModel):
    augments: Optional[List[str]] = Field(...)

class Traits(BaseModel):
    name: str = Field(...)
    num_units: int = Field(...)
    style: int = Field(...)
    tier_current: int = Field(...)
    tier_total: int = Field(...)

class Info(BaseModel):
    game_datetime: int = Field(...)
    game_length: int = Field(...)
    game_version: str = Field(...)
    participants: Optional[List[str]] = Field(...)
    gold_left: int = Field(...)
    last_round: int = Field(...)
    level: int = Field(...)
    placement: int = Field(...)
    players_eliminated: int = Field(...)
    puuid: str = Field(...)
    time_eliminated: int = Field(...)
    total_damage_to_players: int = Field(...)
    traits: Optional[List[str]] = Field(...)


class Match(BaseModel):
    game_datetime: int = Field(...)
    metadata: Optional[Dict] = Field(...)
    info: Optional[Dict] = Field(...)
