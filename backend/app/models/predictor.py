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


class MDIOutput(BaseModel):
    summarized: str
    metrics: str


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
        dictConfig(LogConfig().dict())

        args: ArgumentParser = ArgumentParser(description='TFTChamp api server')
        print(args)
        args.add_argument('-c', '--config', default='configs/challengers.json', type=str,
                          help='config file path (default: configs/challengers.json)')
        # args.add_argument('-r', '--reload', default=True, type=bool,
        #                   action=BooleanOptionalAction,
        #                   help='dummy (default: None)')
        config = ConfigParser.from_args(args)
        # logger = logging.getLogger("app")
        # self.logger = logger
        self.config = config

    def load_model(self):
        """Loads the model"""
        # self.logger.info("Preloading pipleine")

        # load the model from disk
        if self.config['model_dir']:
            load_path = os.path.join(self.config['model_dir'], "model.pkl")
        else:
            load_path = os.path.join(self.save_dir, "model.pkl")

        logging.info(f'Loading model from: {load_path}')
        
        # https://stackoverflow.com/questions/2121874/python-pickling-after-changing-a-modules-directory/2121918#2121918
        sys.path.append(r'../pipeline')
        # load the model from disk
        with open(load_path, 'rb') as input_file:
            loaded_model = pickle.load(input_file)
            logging.info(loaded_model)
        self.model = loaded_model

    def get_feature_importance(self):
        if hasattr(self.model[-1], 'feature_importances_'):
            feature_names = self.model['column_transformer'].get_feature_names_out(
            )
            feature_importances = pd.Series(
                self.model[-1].feature_importances_, index=feature_names
            ).sort_values(ascending=True)
            # plt.figure(figsize=(13, 18))
            # ax = feature_importances[-50:].plot.barh()  # Top 50
            # ax.set_title(
            #     f"{str(type(self.model[-1]).__name__)} {str('.'.join(self.config['data_loader']['args']['data_path'].split('/')[-1].split('.')[:-1]))} TFT Feature Importances (MDI)")
            # ax.figure.figsize = [13, 25]
            # ax.set_xlabel('correlation against placement')
            # ax.set_ylabel('features')
            # ax.figure.tight_layout()
            # ax.figure.savefig(os.path.join(
            #     self.save_dir, f"{type(self.model[-1]).__name__}_feature_importances.png"), dpi=400)
            # train_report += f"\nget_feature_names_out:\n\n {str(self.model['column_transformer'].get_feature_names_out())}"
            # train_report += f"\nfeature_importances_:\n\n {str(self.model[-1].feature_importances_)}"
            # feature_importances.to_csv(os.path.join(self.save_dir, f"{type(self.model[-1]).__name__}_feature_importances.csv"), index=False)


# Create Singleton
tft_champ_model: Predictor = Predictor()


def get_model():
    return tft_champ_model
