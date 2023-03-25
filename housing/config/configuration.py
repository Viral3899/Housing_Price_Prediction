
import sys
import os

from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.constant import *

from housing.util.util import read_yaml_file
from housing.entity.config_entity import DataIngestionConfig, DataTransforamtionConfig, DataValidationConfig,\
    ModelEvaluationConfig, ModelPusherConfig, ModelTrainerConfig, TrainingPipelineConfig


class ConConfiguration:
    def __init__(self, config_file_path=CONFIG_FILE_PATH,
                 current_time_stamp=get_current_time_stamp()) -> None:
        self.config_info = read_yaml_file(file_path=config_file_path)
        self.time_stamp = current_time_stamp
        self.training_pipeline_cofig = self.get_training_pipeline_config()

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        pass

    def get_data_validation_config(self) -> DataValidationConfig:
        pass

    def get_data_transforamtion_config(self) -> DataTransforamtionConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_pipline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(
                ROOT_DIR, training_pipline_config[TRAINING_PIPELINE_NAME_KEY], training_pipline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_pipline_config = TrainingPipelineConfig(
                artifact_dir=artifact_dir)

            logging.info(
                f"Training Pipeline Config: {training_pipline_config}")

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
        raise HousingException(e, sys)
