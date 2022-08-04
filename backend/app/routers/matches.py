from enum import Enum
from fastapi import APIRouter, Body, Request, Response, HTTPException, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Tuple

from models.match import Match

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


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(5, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(20, limit)
    return (skip, capped_limit)


@router.get("/", response_description="List all matches", response_model=List[Match])
async def list_matches(request: Request, platform: Platform = 'oc1', pagination: Tuple[int, int] = Depends(pagination)):
    skip, limit = pagination
    query = request.app.database[f"{platform}_challengers_12.14.456.5556_matches"].find(
        {}, skip=skip, limit=limit)
    results = [Match(**raw_post) async for raw_post in query]
    return results


@router.get("/{id}", response_description="Get a single match by id", response_model=Match)
async def find_match(id: str, request: Request, platform: Platform = 'oc1'):
    if (match := request.app.database[f"{platform}_matches_detail"].find_one({"_id": id})) is not None:
        return match

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Match with ID {id} not found")
