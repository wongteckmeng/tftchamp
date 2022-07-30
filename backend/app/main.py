import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient

from routers.matchdetails import router as matchdetails_router
from routers.matches import router as matches_router
from config import settings

app = FastAPI()
app.include_router(matchdetails_router, tags=[
                   "matchdetails"], prefix="/matchdetail")
app.include_router(matches_router, tags=[
                   "matches"], prefix="/match")


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(settings.db_uri)
    app.database = app.mongodb_client[settings.db_name]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
