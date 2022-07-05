import asyncio
import os
import os.path
import json
import compress_json
import pandas as pd
from datetime import datetime, timedelta
from typing import List

from pyot.core.queue import Queue
from pyot.conf.model import activate_model, ModelConf
from pyot.conf.pipeline import activate_pipeline, PipelineConf


from pyot.utils.itertools import frozen_generator

from utils.configuration import settings
from utils.logger import logging

ASSETS_DIR = settings.assets_dir
API_KEY = settings.api_key
SERVER = 'na1'  # euw1 na1 kr oc1
LEAGUE = 'challengers' # challengers grandmasters 

@activate_model("tft")
class TftModel(ModelConf):
    default_platform = "na1"
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"

@activate_model("lol")
class LolModel(ModelConf):
    default_platform = "na1"
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"

@activate_pipeline("tft")
class TftPipeline(PipelineConf):
    name = "tft_main"
    default = True
    stores = [
        {
            "backend": "pyot.stores.omnistone.Omnistone",
            # "expirations": {
            #     "summoner_v4_by_name": 100,
            #     "match_v4_match": 600,
            #     "match_v4_timeline": 600,
            # }
        },
        {
            "backend": "pyot.stores.cdragon.CDragon",
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "api_key": os.environ["RIOT_API_KEY"],
        }
    ]

from pyot.models import tft
from pyot.utils.lol.routing import platform_to_region

async def get_puuid(summoner: tft.Summoner):
    summoner = await summoner.get()
    return summoner.puuid


async def pull_puuids():
    async with Queue() as queue:
        await queue.put(tft.ChallengerLeague(platform="na1").get())
        await queue.put(tft.MasterLeague(platform="na1").get())
        # Param is optional, used for typing only
        leagues = await queue.join(tft.ChallengerLeague)

        summoners = []
        for league in leagues:
            for entry in league.entries:
                summoners.append(entry.summoner)

        for summoner in summoners:
            await queue.put(get_puuid(summoner))
        return await queue.join(str)


async def get_match_ids(name: str, platform: str) -> List[str]:
    summoner = await tft.Summoner(name=name, platform=platform).get()
    match_history = await tft.MatchHistory(
        puuid=summoner.puuid,
        region=platform_to_region(summoner.platform)
    ).query(
        count=100,
        queue=420,
        start_time=datetime.now() - timedelta(days=200)
    ).get()
    return match_history.ids


async def get_matches():
    matches = list_with_30k_matches
    matches = frozen_generator(matches)  # Freezes the list to prevent mutation
    async with Queue() as queue:
        for match in matches:
            await queue.put(consume_match(match))


async def consume_match(match):
    match.get()  # pass the session to reuse
    # ...
    # Consume your match (e.g. get specific stat, mutate a dictionary, save to db, etc.) ...
    # ...
    return None
    # OR no return (When no return is stated, returns None by default)

async def main():
    o = await tft.ChallengerLeague(platform="na1").get()
    print(o)

if __name__ == '__main__':
    asyncio.run(main())