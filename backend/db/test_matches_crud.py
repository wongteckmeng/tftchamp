from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pymongo import MongoClient
from routers.matchdetails import router as matchdetails_router
from config import settings

app = FastAPI()

app.include_router(matchdetails_router, tags=["matchdetails"], prefix="/matchdetails")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(settings.db_uri)
    app.database = app.mongodb_client[settings.db_name + "_test"]


@app.on_event("shutdown")
async def shutdown_event():
    app.database.drop_collection("oc1_matches_detail")
    app.mongodb_client.close()


sample_post = {
    "_id": "OC1_526884682",
    "metadata": {
        "data_version": "string",
        "match_id": "string",
                    "participants": [
                        "string"
                    ]
    },
    "info": {
        "game_datetime": 0,
        "game_length": 0,
        "game_version": "string",
        "participants": [
                        {
                            "augments": [
                                "string"
                            ],
                            "companion": {
                                "content_ID": "string",
                                "skin_ID": 0,
                                "species": "string"
                            },
                            "gold_left": 0,
                            "last_round": 0,
                            "level": 0,
                            "placement": 0,
                            "players_eliminated": 0,
                            "puuid": "string",
                            "time_eliminated": 0,
                            "total_damage_to_players": 0,
                            "traits": [
                                {
                                    "name": "string",
                                    "num_units": 0,
                                    "style": 0,
                                    "tier_current": 0,
                                    "tier_total": 0
                                }
                            ],
                            "units": [
                                {
                                    "character_id": "string",
                                    "itemNames": [
                                        "string"
                                    ],
                                    "items": [
                                        0
                                    ],
                                    "name": "string",
                                    "rarity": 0,
                                    "tier": 0
                                }
                            ]
                        }
        ],
        "queue_id": 0,
        "tft_game_type": "string",
        "tft_set_core_name": "string",
        "tft_set_number": 0
    }
}


def test_create_match():
    with TestClient(app) as client:
        response = client.post("/match/", json=sample_post)
        assert response.status_code == 201

        body = response.json()
        assert body.get("info").get("tft_game_type") == "string"
        assert body.get("info").get("tft_set_core_name") == "string"
        assert body.get("info").get("tft_set_number") == 0
        assert "_id" in body


def test_create_match_missing_match_id():
    with TestClient(app) as client:
        response = client.post(
            "/match/", json={
                "metadata": {
                    "data_version": "string",
                    "participants": [
                        "string"
                    ]
                }
            })
        assert response.status_code == 422


def test_get_match():
    with TestClient(app) as client:
        new_match = client.post(
            "/match/", json=sample_post).json()
        print(new_match)
        get_match_response = client.get("/match/" + new_match.get("_id"))
        assert get_match_response.status_code == 200
        assert get_match_response.json() == new_match


def test_get_match_unexisting():
    with TestClient(app) as client:
        get_match_response = client.get("/match/unexisting_id")
        assert get_match_response.status_code == status.HTTP_404_NOT_FOUND


def test_update_match():
    with TestClient(app) as client:
        new_match = client.post(
            "/match/", json=sample_post).json()
        sample_post["metadata"]["data_version"] = "Don Quixote 1"
        response = client.put("/match/" + new_match.get("_id"),
                              json=sample_post)
        assert response.status_code == 200
        assert response.json().get("metadata").get("data_version") == "Don Quixote 1"


def test_update_match_unexisting():
    with TestClient(app) as client:
        update_match_response = client.put(
            "/match/unexisting_id", json=sample_post)
        assert update_match_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_match():
    with TestClient(app) as client:
        new_match = client.post(
            "/match/", json=sample_post).json()

        delete_match_response = client.delete("/match/" + new_match.get("_id"))
        assert delete_match_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_match_unexisting():
    with TestClient(app) as client:
        delete_match_response = client.delete("/match/unexisting_id")
        assert delete_match_response.status_code == status.HTTP_404_NOT_FOUND
