from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from models.match import Match

router = APIRouter()


@router.get("/", response_description="List all matches", response_model=List[Match])
async def list_matches(request: Request):
    matches = list(request.app.database["oc1_matches_detail"].find(limit=5))
    return matches


@router.get("/{id}", response_description="Get a single match by id", response_model=Match)
async def find_match(id: str, request: Request):
    if (match := request.app.database[f"oc1_matches_detail"].find_one({"_id": id})) is not None:
        return match

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Match with ID {id} not found")
