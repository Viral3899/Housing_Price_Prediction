import os
import sys
import pandas as ps
import numpy as np


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


from housing.constant import *
from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig
from housing.config.configuration import Configuration
from housing.util.util import read_yaml_file


class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                X[:, self.households_ix]

            population_per_household = X[:,
                                         self.population_ix] / X[:, self.households_ix]

            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                    X[:, self.total_rooms_ix]

                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]

            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e


class DataTransformation:

    def __init__(self,) -> None:
        pass

    def __del__(self):

        logging.info(
            f"\n\n{'='*20} Data Transformation Log Completed {'='*20} \n\n")
