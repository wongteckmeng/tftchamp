import os.path
import compress_json

from .configuration import settings
from .logger import logging

ASSETS_DIR = settings.assets_dir
SERVER = settings.server


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


def load_matches(df, server=SERVER):
    matches_asset = []
    for _, summoner in df.iterrows():
        match_asset = read_json(
            filename='matches_detail' + '_' + server + '_'+summoner['name'])
        if match_asset != None:
            matches_asset.extend(match_asset)

    return matches_asset

def load_summoners(df, server=SERVER):
    matches_asset = []
    for _, summoner in df.iterrows():
        match_asset = read_json(
            filename='matches_detail' + '_' + server + '_'+summoner['name'])
        if match_asset != None:
            matches_asset.extend(match_asset)

    return matches_asset