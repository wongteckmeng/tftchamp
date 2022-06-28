import asyncio
import os.path
import json
import compress_json
import pandas as pd

from pantheon import pantheon

from utils.configuration import settings
from utils.logger import logging

API_KEY = settings.api_key
SERVER = "na1"
ASSETS_DIR = 'assets'
MAX_COUNT = 50


def requestsLog(url, status, headers):
    logging.info(f'status:{status} {url}')
    logging.debug(headers)


panth = pantheon.Pantheon(
    SERVER, API_KEY, requests_logging_function=requestsLog, debug=True)


async def getSummonerId(name):
    try:
        data = await panth.get_summoner_by_name(name)
        return (data['id'], data['accountId'], data['puuid'])
    except Exception as e:
        logging.error(e)


async def getTFTRecentMatchlist(puuid, count=MAX_COUNT):
    try:
        data = await panth.get_tft_matchlist(puuid, count=count)
        return data
    except Exception as e:
        logging.error(e)


async def getTFTRecentMatches(puuid, uniq_matches_id=[]):
    try:
        matchlist = await getTFTRecentMatchlist(puuid)
        # Get only unique new matches from left hand side
        new_matchlist = set(matchlist) - set(uniq_matches_id)
        logging.info(f'Fetching ** {len(new_matchlist)} ** new matches')

        tasks = [panth.get_tft_match(match)
                 for match in new_matchlist]
        return await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(e)


async def getTFTChallengerLeague():
    try:
        data = await panth.get_tft_challenger_league()
        return data
    except Exception as e:
        logging.error(e)


async def getTFTGrandmasterLeague():
    try:
        data = await panth.get_tft_grandmaster_league()
        return data
    except Exception as e:
        logging.error(e)


async def getTFTMasterLeague():
    try:
        data = await panth.get_tft_master_league()
        return data
    except Exception as e:
        logging.error(e)


async def getTFT_Summoner(summonerId):
    try:
        data = await panth.get_tft_summoner(summonerId)
        return data
    except Exception as e:
        logging.error(e)


def get_data_filename(filename='json_data'):
    return os.path.join(ASSETS_DIR, filename+".json.gz")


def write_json(data, filename='json_data', update=False):
    json_asset = os.path.join(ASSETS_DIR, filename+".json.gz")
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


def get_league(league='challengers'):
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

    loop = asyncio.get_event_loop()

    summoners = loop.run_until_complete(getTFTLeagueFunc())
    write_json(summoners, filename=SERVER + '_' + league)

    summoners_league = json.loads('[]')

    for _, summoner in enumerate(summoners['entries'][:]):
        summoner_detail = loop.run_until_complete(
            getTFT_Summoner(summoner['summonerId']))
        if summoner_detail != None:
            summoners_league.append(summoner_detail)

    write_json(summoners_league, filename='summoners_' + SERVER + '_' + league)

    summoners_league_df = pd.json_normalize(summoners_league)
    summoners_df = pd.json_normalize(summoners['entries'])

    return summoners_league_df.merge(
        summoners_df, left_on='id', right_on='summonerId')


if __name__ == '__main__':
    logging.info(f'SERVER: {SERVER} MAX_COUNT: {MAX_COUNT} run.')

    loop = asyncio.get_event_loop()

    summoners_df = get_league(league='challengers')

    # Get all unique matches_id from assets dir
    matches_asset = load_matches(summoners_df)
    matches_id = [match['metadata']['match_id'] for match in matches_asset]
    seen = set()
    uniq_matches_id = [
        x for x in matches_id if x not in seen and not seen.add(x)]

    # For each summoners, get MAX_COUNT recent matches. Extend if any new.
    new_counter = 0
    for index, summoner in summoners_df.iterrows():
        matches_detail = loop.run_until_complete(
            getTFTRecentMatches(summoner['puuid'], uniq_matches_id=uniq_matches_id))
        if matches_detail != None:
            new_counter += len(matches_detail)
            write_json(matches_detail, filename='matches_detail' + '_' + SERVER +
                       '_'+summoner['name'], update=True)

    logging.info(f'new_counter: {new_counter} new matches done.')
    logging.info(f'Number of summoners: {len(summoners_df.index)}.')
