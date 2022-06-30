#!/usr/bin/env python
# coding: utf-8

from wrappers import *

from sklearn.svm import SVC
from sklearn.ensemble import ExtraTreesClassifier, VotingClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures

from sklearn.linear_model import Ridge
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier

# Soft Voting/Majority Rule classifier for unfitted estimators.
clf1 = ExtraTreesClassifier(n_estimators=300, class_weight="balanced")
clf2 = XGBClassifier(objective="binary:logistic",
                     eval_metric="auc", n_estimators=500, max_depth=12)
clf3 = MLPClass()
# clf3 = MLPClassifier(hidden_layer_sizes=(100, 50, 25, 10), max_iter=1000, early_stopping=True)


eclf = VotingClassifier(estimators=[
    ('et', clf1), ('xgb', clf2), ('mlp', clf3)], voting='soft')

methods_dict = {
    'ridge': Ridge,
    'pf': PolynomialFeatures,
    'scaler': StandardScaler,
    'preprocessing': NoShowPreprocessing,
    'column_transformer': Column_Wrapper,
    'PLS': PLSRegressionWrapper,
    'MLPClass': MLPClass,
    'GNB': GaussianNB,
    'SVC': SVC,
    'PCA': PCA,
    'ETC': ExtraTreesClassifier,
    'MLP': MLPClassifier,
    'XGB': XGBClassifier,
    'VCL': eclf,
}
