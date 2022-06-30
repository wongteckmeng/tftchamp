from base import BaseDataLoader
from data_loaders import data_handler
from utils import load_db
from utils.logger import logging

from sklearn.datasets import load_iris, make_classification
from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd  # data processing


class TestClassification(BaseDataLoader):
    """Test case for classification pipeline
    """

    def __init__(self, data_path, shuffle, test_split, random_state, stratify, training, label_name):
        '''set data_path in configs if data localy stored'''

        X, y = load_iris(return_X_y=True)
        data_handler.X_data = X
        data_handler.y_data = y

        super().__init__(data_handler, shuffle, test_split, random_state, stratify, training)


class TestKerasClassification(BaseDataLoader):
    """Test case for keras classification pipeline
    """

    def __init__(self, data_path, shuffle, test_split, random_state, stratify, training, label_name):
        '''set data_path in configs if data localy stored'''

        X, y = make_classification(1000, 20, n_informative=10, random_state=0)
        data_handler.X_data = X.astype(np.float32)
        data_handler.y_data = y.astype(np.int64)

        super().__init__(data_handler, shuffle, test_split, random_state, stratify, training)
