import sys
import os

from housing.logger.logger import logging
from housing.exception.exception import HousingException
from housing.entity.config_entity import DataValidationConfig

from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.config.configuration import Configuration


class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig,

                 data_ingestion_artifact: DataIngestionArtifact) -> None:
        try:
            logging.info(
                f"\n\n{'='*20} Data Validation log Started {'='*20}\n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info(
                'Checking if Training And Testing File is Available!!!!?')
            is_train_file_exists = False
            is_test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            logging.info(
                f'Training File Available Status [is_train_file_exists = {is_train_file_exists}]')

            is_test_file_exists = os.path.exists(test_file_path)
            logging.info(
                f'Testing File Available Status [is_test_file_exists = {is_test_file_exists}]')

            is_availabel = is_train_file_exists and is_test_file_exists

            logging.info(
                f'Training and Testing both File Available Status [is_Avilable = {is_availabel}]')
            
            return is_availabel

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e
        

    def validate_dataset_schema() -> bool:
        validation_status=False






        validation_status=True
        return validation_status

    def initiate_data_validate(self) -> DataValidationArtifact:
        try:
            is_available = self.is_train_test_file_exists()

            if not is_available:
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path
                message = f'Training File : [{train_file_path}] or\n Testing File : [{test_file_path}] is not present.'

                logging.info(message)
                raise Exception (message)
            
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e
