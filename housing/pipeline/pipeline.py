import sys
import os


from housing.config.configuration import Configuration
from housing.exception.exception import HousingException
from housing.logger.logger import logging

from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation


class Pipeline:
    def __init__(self, config: Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(
                data_ingestion_config=self.config.get_data_ingestion_config())

            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(
            ), data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def start_data_transformation(self,
                                  data_ingetion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact) -> DataValidationArtifact:
        try:
            data_transformatin =DataTransformation(data_transformation_config=self.config.get_data_transforamtion_config(),
                                                   data_ingestion_artifact=data_ingetion_artifact,
                                                   data_validation_artifact=data_validation_artifact)
            
            return data_transformatin.initiate_data_transformation()
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def start_model_trainer(self):
        pass

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:

            data_ingestion_artifact = self.start_data_ingestion()
            data_valiadtion_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            data_transforamtion_artifcat = self.start_data_transformation(
                data_ingetion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_valiadtion_artifact
            )
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e
