import os
import sys
import pandas as pd



from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor


from housing.logger.logger import logging
from housing.exception.exception import HousingException
from housing.util.util import read_yaml_file,save_object,load_numpy_array_data
from housing.config.configuration import DataIngestionConfig,DataTransformationConfig,DataValidationConfig,ModelTrainerConfig
from housing.entity.config_entity import DataValidationConfig,DataIngestionConfig,DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact,ModelTrainerArtifact
from housing.entity.model_factory import ModelFactory




class ModelTrainer:

    def __init__(self,model_trainer_config: ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact) -> None:
        try:
            logging.info(
                f"\n\n{'='*20} Model Trainer log Started {'='*20}\n\n")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
            
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e,sys)
        

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        
        logging.info('loading Transformed Training and Testing Data...')

        transformed_train_file_path = self.data_transformation_artifact.transformed_train_file_path
        train_array = load_numpy_array_data(transformed_train_file_path)

        transformed_test_file_path = self.data_transformation_artifact.transformed_test_file_path
        test_array = load_numpy_array_data(transformed_test_file_path)


        logging.info('Splitting Training and Testing Data... into Input and Target Colums')

        X_train,y_train, X_test, y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]

        logging.info('Extracting Model Config File')
        model_config_file = self.model_trainer_config.model_config_file_path

        logging.info('Start finding Best Model using Model Factory Class')
        base_accuracy = self.model_trainer_config.base_accuracy
        logging.info(f"Expected(Base) accuracy Should be {base_accuracy}")

        best_model = ModelFactory()
