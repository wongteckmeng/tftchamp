import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient

from routes import router as match_router
from config import settings

app = FastAPI()
app.include_router(match_router, tags=["matches"], prefix="/match")


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
