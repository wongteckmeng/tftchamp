import argparse
import asyncio
import collections
import os.path
import json
from typing import Dict, List

import compress_json
import pandas as pd
from pandas import DataFrame

from pantheon import pantheon

from utils.configuration import settings
from utils.parse_config import ConfigParser
from utils.logger import logging

LOAD_NEW: bool = False
ASSETS_DIR: str = settings.assets_dir
API_KEY: str = settings.api_key
SERVER = 'na1'  # ['euw1', 'na1', 'kr', 'oc1']
LEAGUE = 'challengers'  # ['challengers', 'grandmasters']

MAX_COUNT: int = 30


def requestsLog(url, status, headers):
    logging.info(f'status:{status} {url}')
    logging.debug(headers)


async def main(config: ConfigParser):
    LOAD_NEW: bool = config["load_new"]
    SERVER: str = config["server"]
    LEAGUE: str = config["league"]
    MAX_COUNT: int = config["max_count"]

    # create Patheon object to 1 server API key
    Panth = pantheon.Pantheon(
        SERVER, API_KEY, requests_logging_function=requestsLog, debug=True)

    async def getSummonerId(name):
        try:
            data = await Panth.get_summoner_by_name(name)
            return (data['id'], data['accountId'], data['puuid'])
        except Exception as e:
            logging.error(e)

    async def getTFTRecentMatchlist(puuid, count=MAX_COUNT):
        try:
            data: List[str] = await Panth.get_tft_matchlist(puuid, count=count)
            return data
        except Exception as e:
            logging.error(e)
            return []

    async def getTFTRecentMatches(puuid, uniq_matches_id=[]):
        try:
            matchlist = await getTFTRecentMatchlist(puuid)
            # Get only unique new matches from left hand side
            new_matchlist: set = set(matchlist) - set(uniq_matches_id)
            logging.info(f'Fetching ** {len(new_matchlist)} ** new matches')

            tasks: list = [Panth.get_tft_match(match)
                           for match in new_matchlist]
            # Extend new matches
            uniq_matches_id.extend(new_matchlist)

            matches: tuple = await asyncio.gather(*tasks)

            return matches if matches is not None else [], uniq_matches_id
        except Exception as e:
            logging.error(e)
            return [], uniq_matches_id

    async def getTFTChallengerLeague():
        try:
            data = await Panth.get_tft_challenger_league()
            return data
        except Exception as e:
            logging.error(e)

    async def getTFTGrandmasterLeague():
        try:
            data = await Panth.get_tft_grandmaster_league()
            return data
        except Exception as e:
            logging.error(e)

    async def getTFTMasterLeague():
        try:
            data = await Panth.get_tft_master_league()
            return data
        except Exception as e:
            logging.error(e)

    async def getTFT_Summoner(summonerId):
        try:
            data = await Panth.get_tft_summoner(summonerId)
            return data
        except Exception as e:
            logging.error(e)

    def get_data_filename(filename='json_data'):
        return os.path.join(ASSETS_DIR, filename+".json.gz")

    def write_json(data, filename='json_data', update=False):
        json_asset = get_data_filename(filename)
        try:
            if update:  # Extend json file on update mode
                old_data = read_json(filename)
                data.extend(old_data)

            compress_json.dump(data, json_asset)

        except FileNotFoundError:
            logging.warning(f"{filename} not found.")

    def read_json(filename='json_data'):
        json_asset = get_data_filename(filename)
        try:
            return compress_json.load(json_asset)
        except Exception as e:
            logging.error(e)
            return []

    def load_matches(df):
        matches_asset = []
        for _, summoner in df.iterrows():
            match_asset = read_json(
                filename='matches_detail' + '_' + SERVER + '_'+summoner['name'])
            if match_asset != None:
                matches_asset.extend(match_asset)

        return matches_asset

    async def get_league(league='challengers'):
        """Get league's summoners details.

        Args:
            league (str, optional): TFT league. Defaults to 'challengers'.

        Returns:
            Dataframe: Dataframe of league's summoners details.
            LeagueListDTO
                Name 	Data Type 	Description
                leagueId 	string 	
                entries 	List[LeagueItemDTO] 	
                tier 	string 	
                name 	string 	
                queue 	string 	
                    LeagueItemDTO
                        Name 	Data Type 	Description
                        freshBlood 	boolean 	
                        wins 	int 	First placement.
                        summonerName 	string 	
                        miniSeries 	MiniSeriesDTO 	
                        inactive 	boolean 	
                        veteran 	boolean 	
                        hotStreak 	boolean 	
                        rank 	string 	
                        leaguePoints 	int 	
                        losses 	int 	Second through eighth placement.
                        summonerId 	string 	Player's encrypted summonerId.
                            MiniSeriesDTO
                                Name 	Data Type 	Description
                                losses 	int 	
                                progress 	string 	
                                target 	int 	
                                wins 	int 
        """
        match league:
            case 'challengers':
                getTFTLeagueFunc = getTFTChallengerLeague
            case 'grandmasters':
                getTFTLeagueFunc = getTFTGrandmasterLeague
            case 'masters':
                getTFTLeagueFunc = getTFTMasterLeague
            case _:
                # 0 is the default case if x is not found
                getTFTLeagueFunc = getTFTChallengerLeague

        summoners = await getTFTLeagueFunc()
        write_json(summoners, filename=SERVER + '_' + league)

        summoners_league: List = json.loads('[]')

        for _, summoner in enumerate(summoners['entries'][:]):
            summoner_detail = await getTFT_Summoner(summoner['summonerId'])
            if summoner_detail != None:
                summoners_league.append(summoner_detail)

        write_json(summoners_league, filename='summoners_' +
                   SERVER + '_' + league)

        summoners_league_df = pd.json_normalize(summoners_league)
        summoners_df = pd.json_normalize(summoners['entries'])

        return summoners_league_df.merge(
            summoners_df, left_on='id', right_on='summonerId')

    logging.info(
        f'*** Starting SERVER: {SERVER}, LEAGUE: {LEAGUE}, MAX_COUNT: ** {MAX_COUNT} ** run. ***')

    if LOAD_NEW:
        summoners_df: DataFrame = await get_league(league=LEAGUE)
        summoners_df.to_pickle(os.path.join(
            ASSETS_DIR, f'{SERVER}_{LEAGUE}_summoners.pickle'))
    else:
        summoners_df: DataFrame = pd.read_pickle(os.path.join(
            ASSETS_DIR, f'{SERVER}_{LEAGUE}_summoners.pickle'))
    logging.info(
        f'Loading for ** {len(summoners_df.index)} ** {"new" if LOAD_NEW else "cached"} summoners.')

    # Get all unique matches_id from assets dir
    matches_asset: list = load_matches(summoners_df)
    matches_id: list = [match['metadata']['match_id']
                        for match in matches_asset]
    seen: set = set()
    uniq_matches_id: list = [
        x for x in matches_id if x not in seen and not seen.add(x)]
    logging.info(f'Loaded ** {len(uniq_matches_id)} ** matches.')

    # For each summoners, get MAX_COUNT recent matches. Extend if any new.
    new_counter = 0
    for _, summoner in summoners_df.iterrows():
        matches_detail, uniq_matches_id = await getTFTRecentMatches(summoner['puuid'], uniq_matches_id=uniq_matches_id)
        # or (None, None)
        if (matches_detail != None) and (matches_detail != []):
            new_counter += len(matches_detail)
            write_json(matches_detail, filename='matches_detail' + '_' + SERVER +
                       '_'+summoner['name'], update=True)

    logging.info(f'new_counter: ** {new_counter} ** new matches done.')
    logging.info(f'Number of summoners: ** {len(summoners_df.index)} **.')
    logging.info(f'*** End loading from {SERVER}_{LEAGUE} done. ***')

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='TFT API matches scraper')
    args.add_argument('-c', '--config', default=None, type=str,
                      help='config file path (default: None)')
    # custom cli options to modify configuration from default values given in json file.
    CustomArgs = collections.namedtuple('CustomArgs', 'flags type target')
    options = [
        CustomArgs(['-cv', '--cross_validation'], type=int,
                   target='cross_validation;args;n_repeats'),
    ]
    config = ConfigParser.from_args(args, options)
    print(config["server"])
    asyncio.run(main(config))
