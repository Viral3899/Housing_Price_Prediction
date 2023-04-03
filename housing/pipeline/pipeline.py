import sys
import os


from housing.config.configuration import Configuration
from housing.exception.exception import HousingException
from housing.logger.logger import logging

from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig,ModelTrainerConfig,ModelEvaluationConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
from housing.component.model_evaluation import ModelEvaluation



class Pipeline:
    def __init__(self, config: Configuration = Configuration()) -> None:
        """
        The function takes in a configuration object and sets it to the class variable config
        
        :param config: Configuration = Configuration()
        :type config: Configuration
        """ 
        try:
            self.config = config
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        It takes in a config object, creates a data ingestion object, and then initiates the data
        ingestion process
        :return: DataIngestionArtifact
        """
        try:
            data_ingestion = DataIngestion(
                data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        """
        It takes in a data ingestion artifact and returns a data validation artifact
        
        :param data_ingestion_artifact: This is the object that contains the data that needs to be
        validated
        :type data_ingestion_artifact: DataIngestionArtifact
        """
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(
            ), data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def start_data_transformation(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_artifact: DataValidationArtifact) -> DataValidationArtifact:
        """
        The function takes in two arguments, data_ingestion_artifact and data_validation_artifact, and
        returns a data_validation_artifact
        
        :param data_ingestion_artifact: DataIngestionArtifact
        :type data_ingestion_artifact: DataIngestionArtifact
        :param data_validation_artifact: DataValidationArtifact
        :type data_validation_artifact: DataValidationArtifact
        :return: DataValidationArtifact
        """
        try:
            data_transformation =DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
                                                   data_ingestion_artifact=data_ingestion_artifact,
                                                   data_validation_artifact=data_validation_artifact)
            
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def start_model_trainer(self,data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def start_model_evaluation(self,data_):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        """
        The function runs a pipeline that starts with data ingestion, then data validation, and finally
        data transformation
        """
        try:

            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
