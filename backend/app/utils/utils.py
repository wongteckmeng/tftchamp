import os.path
from pathlib import Path
from collections import OrderedDict
import csv
import json
import compress_json

from .configuration import settings
from .logger import logging

ASSETS_DIR = settings.assets_dir
SERVER = settings.server


def read_csv(data_path):
    with open(data_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)

        data_list = []
        line_count = 0
        for row in csv_reader:
            line_count += 1
            data_list.append(row)
        print(f'Processed {line_count} lines.')
    return data_list


def read_json(fname):
    fname = Path(fname)
    with fname.open('rt') as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    fname = Path(fname)
    with fname.open('wt') as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def get_data_filename(filename='json_data'):
    return os.path.join(ASSETS_DIR, filename+".json.gz")


def write_asset_json(data, filename='json_data', update=False):
    json_asset = get_data_filename(filename)
    try:
        if update:  # Extend json file on update mode
            old_data = read_asset_json(filename)
            data.extend(old_data)

        compress_json.dump(data, json_asset)

    except FileNotFoundError:
        logging.warning(f"{filename} not found.")


def read_asset_json(filename='json_data'):
    json_asset = get_data_filename(filename)
    try:
        return compress_json.load(json_asset)
    except Exception as e:
        logging.error(e)
        return []


def load_matches(df, server=SERVER):
    matches_asset = []
    for _, summoner in df.iterrows():
        match_asset = read_asset_json(
            filename='matches_detail' + '_' + server + '_'+summoner['name'])
        if match_asset != None:
            matches_asset.extend(match_asset)

    return matches_asset


def load_summoners(df, server=SERVER):
    matches_asset = []
    for _, summoner in df.iterrows():
        match_asset = read_asset_json(
            filename='matches_detail' + '_' + server + '_'+summoner['name'])
        if match_asset != None:
            matches_asset.extend(match_asset)

    return matches_asset
