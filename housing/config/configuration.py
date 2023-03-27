
import sys
import os

from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.constant import *

from housing.util.util import read_yaml_file
from housing.entity.config_entity import DataIngestionConfig, DataTransforamtionConfig, DataValidationConfig,\
    ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig, TrainingPipelineConfig


class Configuration:
    def __init__(self, config_file_path=CONFIG_FILE_PATH,
                 current_time_stamp=get_current_time_stamp()) -> None:

        try:
            self.config_info = read_yaml_file(file_path=config_file_path)

            self.training_pipeline_config = self.get_training_pipeline_config()

            self.time_stamp = current_time_stamp

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:

        try:

            training_pipline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]

            artifact_dir = os.path.join(
                ROOT_DIR, training_pipline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                )
            
            training_pipline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)

            logging.info(
                f"Training Pipeline Config: {training_pipline_config}")

            return training_pipline_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        try:
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            artifact_dir = self.training_pipeline_config.artifact_dir

            data_ingestion_artifact_dir = os.path.join(
                artifact_dir, 
                DATA_INGESTION_ARTIFACT_DIR_KEY,
                get_current_time_stamp()
                )

            raw_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
                )

            ingested_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_KEY]
                )

            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
                )

            ingested_train_dir = os.path.join(
                ingested_dir, 
                data_ingestion_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
                )

            ingested_test_dir = os.path.join(
                ingested_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
                )


            data_ingestion_config = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=tgz_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )


            logging.info(f"Data Ingestion Config: {data_ingestion_config}")

            return data_ingestion_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys)
        

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_info=self.config_info[DATA_VALIDATION_CONFIG_KEY]

            artifact_dir=self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir=os.path.join(
                artifact_dir,data_validation_info[DATA_VALIDATON_ARTIFACT_DIR_KEY]
            )
            
            schema_file_path=os.path.join(
                ROOT_DIR,
                data_validation_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            report_file_path=os.path.join(
                data_validation_artifact_dir,
                data_validation_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path=os.path.join(
                data_validation_artifact_dir,
                data_validation_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            data_validation_config=DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path
            )

            return data_validation_config

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e


    def get_data_transforamtion_config(self) -> DataTransforamtionConfig:
        pass


    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass


    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass


    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass
