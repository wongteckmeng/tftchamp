from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from models import MatchDetail, MatchDetailUpdate

router = APIRouter()


@router.post("/", response_description="Create a new match", status_code=status.HTTP_201_CREATED, response_model=MatchDetail)
async def create_match(request: Request, match: MatchDetail = Body(...)):
    match = jsonable_encoder(match)
    new_match = request.app.database["oc1_matches_detail"].insert_one(match)
    created_match = request.app.database["oc1_matches_detail"].find_one(
        {"_id": new_match.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_match)


@router.get("/", response_description="List all matches", response_model=List[MatchDetail])
async def list_matches(request: Request):
    matches = list(request.app.database["oc1_matches_detail"].find(limit=5))
    return matches


@router.get("/{id}", response_description="Get a single match by id", response_model=MatchDetail)
async def find_match(id: str, request: Request):
    if (match := request.app.database["oc1_matches_detail"].find_one({"_id": id})) is not None:
        return match

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"MatchDetail with ID {id} not found")


@router.put("/{id}", response_description="Update a match", response_model=MatchDetail)
async def update_match(id: str, request: Request, match: MatchDetailUpdate = Body(...)):
    match = {k: v for k, v in match.dict().items() if v is not None}

    if len(match) >= 1:
        update_result = request.app.database["oc1_matches_detail"].update_one(
            {"_id": id}, {"$set": match}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"MatchDetail with ID {id} not found")

    if (
        existing_match := request.app.database["oc1_matches_detail"].find_one({"_id": id})
    ) is not None:
        return existing_match

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"MatchDetail with ID {id} not found")


@router.delete("/{id}", response_description="Delete a match")
async def delete_match(id: str, request: Request, response: Response):
    delete_result = request.app.database["oc1_matches_detail"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"MatchDetail with ID {id} not found")
