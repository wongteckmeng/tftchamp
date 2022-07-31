import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from routers.matchdetails import router as matchdetails_router
from routers.matches import router as matches_router
from config import settings

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.db_uri)
    app.database = app.mongodb_client[settings.db_name]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(matchdetails_router, tags=[
                   "matchdetails"], prefix="/matchdetail")
app.include_router(matches_router, tags=[
                   "matches"], prefix="/match")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
