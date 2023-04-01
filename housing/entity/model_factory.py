import os
import sys
import yaml
from collections import namedtuple


from housing.util.util import read_yaml_file
from housing.logger.logger import logging
from housing.exception.exception import HousingException

GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

InitializedModelDetail = namedtuple("InitializedModelDetail",["model_serial_number",
                                                              "model",
                                                              "param_grid_search",
                                                              "model_name"
                                                              ])

GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                             "model",
                                                             "best_model",
                                                             "best_parameters",
                                                             "best_score"
                                                             ])

BestModel = namedtuple("BestModel", ["model_serial_number",
                                     "model",
                                     "best_model",
                                     "best_parameters",
                                     "best_score"
                                     ])

MetricInfoArtifact = namedtuple("MetricInfoArtifact",["model_name",
                                                      "model_object",
                                                      "train_rmse",
                                                      "test_rmse",
                                                      "train_accuracy",
                                                      "test_accuracy",
                                                      "model_accuracy",
                                                      "index_number"
                                                      ])


class ModelFactory:

    def __init__(self, model_config_path: str = None):

        try:
            self.config: dict = ModelFactory.read_params(model_config_path)
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    @staticmethod
    def read_params(config_path: str) -> dict:
        """
        It reads a yaml file and returns a dictionary
        
        :param config_path: str = "config.yaml"
        :type config_path: str
        :return: a dictionary.
        """
        try:
            with open(config_path) as yaml_file:
                config: dict = yaml.safe_load(yaml_file)
            return config
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def excecute_grid_search_operation(self, initialized_model: InitializedModelDetail,
                                        input_feature,output_feature) -> GridSearchedBestModel:
        try:
            logging.info(f"Initiating GridSearchCV class")
            grid_

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)