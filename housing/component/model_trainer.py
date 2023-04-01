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

class HousingEstimatorModel:
    def __init__(self,preprocessing_object, trained_model_object) -> None:
        """
        This function takes in a preprocessing object and a trained model object and assigns them to the
        class variables preprocessing_object and trained_model_object.
        
        :param preprocessing_object: This is the object of the class Preprocessing
        :param trained_model_object: This is the object of the class that contains the trained model
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        
    def predict(self, X):
        
        try:
            transformed_features = self.preprocessing_object(X)
            
            return self.trained_model_object.predict(transformed_features)
        except Exception as e:
            logging.info(f'Error Occurred at {HousingException(e,sys)}')
            raise HousingException(e,sys)
        
    def __repr__(self) -> str:
        return f"{type(self.trained_model_object.__name__)}()"
    
    def __str__(self) -> str:
        return f"{type(self.trained_model_object.__name__)}()"
        
class ModelTrainer:

    def __init__(self,model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact) -> None:
        """
        The function takes in two arguments, a ModelTrainerConfig object and a DataTransformationArtifact
        object. 
        
        The ModelTrainerConfig object is a class that contains the configuration parameters for the model
        trainer. 
        
        The DataTransformationArtifact object is a class that contains the data transformation artifact. 
        
        The function then initializes the model trainer config and data transformation artifact. 
        
        The function also logs the start of the model trainer log. 
        
        The function then raises an exception if an error occurs.
        
        :param model_trainer_config: This is the configuration object that contains all the parameters
        that are required to train the model
        :type model_trainer_config: ModelTrainerConfig
        :param data_transformation_artifact: This is the artifact that is created by the
        DataTransformation class
        :type data_transformation_artifact: DataTransformationArtifact
        """
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
        model_config_file_path= self.model_trainer_config.model_config_file_path

        logging.info('Start finding Best Model using Model Factory Class')
        base_accuracy = self.model_trainer_config.base_accuracy
        logging.info(f"Expected(Base) accuracy Should be {base_accuracy}")

        model_factory = ModelFactory(model_config_path=model_config_file_path)
        
        logging.info(f'Initializing Model Selection operation')
        best_model = model_factory.get_best_model(X=X_train,y=y_train,base_accuracy=base_accuracy)
