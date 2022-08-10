from enum import Enum
from fastapi import APIRouter, Body, Request, Response, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Tuple

from models.match import Match, MatchResult
from config import settings

router = APIRouter()


class Platform(str, Enum):
    euw1 = "euw1",
    br1 = "br1",
    eun1 = "eun1",
    jp1 = "jp1",
    kr = "kr",
    la1 = "la1",
    la2 = "la2",
    na1 = "na1",
    oc1 = "oc1",
    tr1 = "tr1",
    ru = "ru"

class League(str, Enum):
    challengers = "challengers",
    grandmasters = "grandmasters",
    masters = "masters",
    diamonds = "diamonds"

async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(5, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@router.get("/", response_description="List all matches", response_model=MatchResult) #List[Match]
async def list_matches(request: Request, platform: Platform = 'oc1', pagination: Tuple[int, int] = Depends(pagination)):
    skip, limit = pagination
    count = await request.app.database[f"{platform}_challengers_{settings.latest_release}_matches"].count_documents({})
    print(f'count: {count}')
    query = request.app.database[f"{platform}_challengers_{settings.latest_release}_matches"].find(
        {}, skip=skip, limit=limit)
    results = [Match(**raw_post) async for raw_post in query]
    response: MatchResult = {"count": count, "result": results}
    return response


@router.get("/{id}", response_description="Get a single match by id", response_model=Match)
async def find_match(id: str, request: Request, platform: Platform = 'oc1'):
    if (match := request.app.database[f"{platform}_matches_detail"].find_one({"_id": id})) is not None:
        return match

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Match with ID {id} not found")
