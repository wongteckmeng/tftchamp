import argparse
import asyncio
import collections
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from logging.config import dictConfig
import logging

from motor.motor_asyncio import AsyncIOMotorClient

from routers.matchdetails import router as matchdetails_router
from routers.matches import router as matches_router
from routers.predictors import model_router as predictors_router
from config import settings
from utils.parse_config import ConfigParser

from config import LogConfig, get_settings
dictConfig(LogConfig().dict())
logger = logging.getLogger("app")

app: FastAPI = FastAPI(title=get_settings().app_name)
args = None
options = None
config = None

@app.on_event("startup")
async def startup_db_client():
    print(f"startup_db_client: {config}")
    app.mongodb_client = AsyncIOMotorClient(settings.db_uri)
    app.mongodb_client.get_io_loop = asyncio.get_running_loop
    app.database = app.mongodb_client[settings.db_name]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Middleware
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=False,
                   allow_methods=['*'],
                   allow_headers=['*'])

# Routers
app.include_router(matchdetails_router, tags=[
                   "matchdetails"], prefix="/matchdetail")
app.include_router(matches_router, tags=[
                   "matches"], prefix="/match")
app.include_router(predictors_router, tags=[
                   "predictors"])


async def main(config):
    print(f"main: {config}")
    app.config = config
    config = uvicorn.Config(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )

    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    args = argparse.ArgumentParser(description='TFTChamp Server')
    args.add_argument('-c', '--config', default=None, type=str,
                      help='config file path (default: None)')

    # custom cli options to modify configuration from default values given in json file.
    CustomArgs = collections.namedtuple('CustomArgs', 'flags type target')
    options = [
        CustomArgs(['-cv', '--cross_validation'], type=int,
                   target='cross_validation;args;n_repeats'),
    ]
    config = ConfigParser.from_args(args, options)
    asyncio.run(main(config))
