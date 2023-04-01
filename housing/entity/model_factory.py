import os
import sys
import yaml
from collections import namedtuple
import importlib


from housing.util.util import read_yaml_file
from housing.logger.logger import logging
from housing.exception.exception import HousingException

GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

InitializedModelDetail = namedtuple("InitializedModelDetail", ["model_serial_number",
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

MetricInfoArtifact = namedtuple("MetricInfoArtifact", ["model_name",
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
        """
        The function reads a config file and initializes a model object.

        :param model_config_path: str = None
        :type model_config_path: str
        """

        try:
            self.config: dict = ModelFactory.read_params(model_config_path)
            self.grid_search_cv_module: str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_cv_class_name: str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_cv_property_data: dict = self.config[GRID_SEARCH_KEY][PARAM_KEY]

            self.model_initialization_config: dict = dict(
                self.config[MODEL_SELECTION_KEY])

            self.initialized_model_list = None
            self.grid_searched_best_model_list = None

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

    @staticmethod
    def update_property_of_class(instance_ref: object, property_data: dict):
        """
        It takes an instance of a class and a dictionary of properties and values and updates the
        instance with the values in the dictionary

        :param instance_ref: object
        :type instance_ref: object
        :param property_data: {'name': 'test', 'age': 'test', 'gender': 'test', 'address': 'test',
        'phone': 'test', 'email': 'test', 'password': 'test', 'confirm_password': 'test'}
        :type property_data: dict
        """
        try:
            if not isinstance(property_data, dict):
                raise Exception(
                    "property_data parameter required to dictionary")
            print(property_data)
            for key, value in property_data.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref, key, value)
            return instance_ref
        except Exception as e:
            logging.info(f'Error Occurred at {HousingException(e,sys)}')
            raise HousingException(e, sys)

    @staticmethod
    def class_for_name(module_name: str, class_name: str):
        """
        It takes a string of the module name and a string of the class name and returns the class object

        :param module_name: The name of the module you want to import
        :type module_name: str
        :param class_name: The name of the class you want to instantiate
        :type class_name: str
        :return: The class reference
        """
        try:
            # load the Module ,IF Module there is not will raise ImportError
            module = importlib.import_module(module_name)
            # get the class, will raise AttributeError if class cannot be found
            logging.info(f"Executing command: from {module} import {class_name}")
            class_ref = getattr(module, class_name)
            return class_ref
        except Exception as e:
            logging.info(f'Error Occurred at {HousingException(e,sys)}')
            raise HousingException(e, sys)

    def execute_grid_search_operation(self, initialized_model: InitializedModelDetail,
                                      input_feature, output_feature) -> GridSearchedBestModel:
        try:
            grid_search_cv_ref = ModelFactory.class_for_name(module_name=self.grid_search_cv_module,
                                                             class_name=self.grid_search_cv_class_name
                                                             )
            grid_search_cv_model = grid_search_cv_ref(estimator=initialized_model.model,
                                                      param_grid=initialized_model.model_serial_number
                                                      )
            grid_search_cv = ModelFactory.update_property_of_class(grid_search_cv_model,
                                                                   self.grid_search_cv_property_data
                                                                   )
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__} Started." {"<<"*30}'
            logging.info(message)
            grid_search_cv.fit(input_feature,output_feature)
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__}" completed {"<<"*30}'
            grid_searched_best_model = GridSearchedBestModel(model_serial_number=initialized_model.model_serial_number,
                                                             model=initialized_model.model,
                                                             best_model=grid_search_cv.best_estimator_,
                                                             best_parameters=grid_search_cv.best_params_,
                                                             best_score=grid_search_cv.best_score_
                                                             )
            return grid_searched_best_model
            
        except Exception as e:
            logging.info(f'Error Occurred at {HousingException(e,sys)}')
            raise HousingException(e, sys)
        
    def get_initialized_model_list():
        pass

    def get_best_model(self, X, y, base_accuracy):
        try:
            logging.info('Started Initializing model from config File')
            initialized_model_list = self.get_initialized_model_list()
        except Exception as e:
            logging.info(f'Error Occurred at {HousingException(e,sys)}')
            raise HousingException(e, sys)
