from argparse import ArgumentParser
import os
import sys
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from logging.config import dictConfig
import pickle
# import wrappers
import pandas as pd
# import matplotlib.pyplot as plt

import logging
# from utils.logger import logging

from config import LogConfig, get_settings
from utils.parse_config import ConfigParser

import uuid


class MongoBaseModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id", examples=[
                    'NA1_4387530978-wgvrKfcuCGDmgyrUmiXknS41acg6Y26hfQwsXNj_eJ86Tv8_Bb7SBOUVSQqI1JdyBSmq92XGDrGYHA'])


class FeatureImportanceOutput(BaseModel):
    results: List[dict] = []
    # label: List[str] = []
    # feature_importance: List[float] = []


class MetadataOutput(BaseModel):
    latest_version: str = Field(..., examples=[
                                '12.15.458.1416'], title='The latest_version Schema')
    latest_patch: str = Field(..., examples=[
                              '2022-08-10'], title='The latest_patch Schema')


class ImagesList(BaseModel):
    results: List[dict] = []


class Text(MongoBaseModel):
    text: str = Field(
        ..., examples=['Description'], title='The text Schema'
    )


class Image(Text):
    image: bytes = Field(..., examples=[
        None], title='The Image Schema')


class PredictionInput(BaseModel):
    text: str
    reference: str
    modelId: str


class PredictionOutput(BaseModel):
    summarized: str
    metrics: str


class Predictor():
    config: Optional[Any]
    model: Optional[Any]
    targets: Optional[List[str]]

    def __init__(self):
        args: ArgumentParser = ArgumentParser(
            description='TFTChamp api server')
        args.add_argument('-c', '--config', default='configs/challengers.json', type=str,
                          help='config file path (default: configs/challengers.json)')
        config = ConfigParser.from_args(args)

        dictConfig(LogConfig().dict())
        logger = logging.getLogger("app")
        self.logger = logger
        self.config = config

    def load_model(self):
        """Loads the model"""
        # self.logger.info("Preloading pipleine")

        # load the model from disk
        if self.config['model_dir']:
            load_path = os.path.join(self.config['model_dir'], "model.pkl")
        else:
            load_path = os.path.join(self.save_dir, "model.pkl")

        self.logger.info(f'Loading model from: {load_path}')

        # https://stackoverflow.com/questions/2121874/python-pickling-after-changing-a-modules-directory/2121918#2121918
        sys.path.append(r'../pipeline')
        # load the model from disk
        with open(load_path, 'rb') as input_file:
            loaded_model = pickle.load(input_file)
            logging.info(loaded_model)
        self.model = loaded_model

    def get_feature_importance(self):

        if hasattr(self.model[-1], 'feature_importances_'):
            feature_names = self.model['column_transformer'].get_feature_names_out()
            feature_importances = []
            for index, feature_name in enumerate(feature_names[-50:], -50):
                feature_importances.append({'label': feature_name, 'feature_importance': self.model[-1].feature_importances_[index].item()})
                if index >= 50:
                    break

            return feature_importances
            # return self.model[-1].feature_importances_[-50:].tolist(), feature_names[-50:].tolist()
        else:
            return []

    def predict(self, input: PredictionInput) -> PredictionOutput:
        """Predict input(x) to (y)"""
        if not self.model:
            raise RuntimeError("Model is not loaded")

        self.logger.info(input)


# Create Singleton
tft_champ_model: Predictor = Predictor()


def get_model():
    return tft_champ_model
