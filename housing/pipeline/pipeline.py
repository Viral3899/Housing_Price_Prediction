import sys
import os
import pandas as pd
from collections import namedtuple
import uuid

from threading import Thread
from housing.config.configuration import Configuration
from housing.exception.exception import HousingException
from housing.logger.logger import logging

from housing.constant import *
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig,ModelTrainerConfig,ModelEvaluationConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
from housing.component.model_evaluation import ModelEvaluation
from housing .component.model_pusher import ModelPusher

Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                       "running_status", "start_time", "stop_time", "execution_time", "message",
                                       "experiment_file_path", "accuracy", "is_model_accepted"])



class Pipeline(Thread):
    experiment: Experiment = Experiment(experiment_id=None, initialization_timestamp=None,artifact_time_stamp=None,
                                        running_status=None,start_time=None,stop_time=None,execution_time=None,message=None,
                                        experiment_file_path=None,accuracy=None,is_model_accepted=None
                                        )
    experiment_file_path = None
    
    def __init__(self, config: Configuration = Configuration()) -> None:
        """
        The function takes in a configuration object and sets it to the class variable config
        
        :param config: Configuration = Configuration()
        :type config: Configuration
        """ 
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok=True)
            Pipeline.experiment_file_path=os.path.join(config.training_pipeline_config.artifact_dir,EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME)
            super().__init__(daemon=False, name="pipeline")
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

    def start_model_evaluation(self,data_ingestion_artifact: DataIngestionArtifact,
                               data_validation_artifact : DataValidationArtifact,
                               model_trainer_artifact : ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_evaluator = ModelEvaluation(
                model_evaluation_config=self.config.get_model_evaluation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact
                                              )
            return model_evaluator.initiate_model_evaluation()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.config.get_model_pusher_config(),
                model_evaluation_artifact=model_evaluation_artifact
            )
            return model_pusher.initiate_model_pusher()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def run_pipeline(self):
        """
        The function runs a pipeline that starts with data ingestion, then data validation, and finally
        data transformation
        """
        try:
            if Pipeline.experiment.running_status:
                logging.info("Pipeline is already running")
                return Pipeline.experiment
            # data ingestion
            logging.info("Pipeline starting.")

            experiment_id = str(uuid.uuid4())

            Pipeline.experiment = Experiment(experiment_id=experiment_id,
                                             initialization_timestamp=self.config.time_stamp,
                                             artifact_time_stamp=self.config.time_stamp,
                                             running_status=True,
                                             start_time=datetime.now(),
                                             stop_time=None,
                                             execution_time=None,
                                             experiment_file_path=Pipeline.experiment_file_path,
                                             is_model_accepted=None,
                                             message="Pipeline has been started.",
                                             accuracy=None,
                                             )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")

            self.save_experiment()

            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(model_trainer_artifact=model_trainer_artifact,
                                                                    data_ingestion_artifact=data_ingestion_artifact,
                                                                    data_validation_artifact=data_validation_artifact)
            print(model_evaluation_artifact)
            
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
                logging.info(f'Model pusher artifact: {model_pusher_artifact}')
            else:
                logging.info("Trained model rejected.")
            logging.info("Pipeline completed.")
            
            stop_time = datetime.now()
            Pipeline.experiment = Experiment(experiment_id=Pipeline.experiment.experiment_id,
                                             initialization_timestamp=self.config.time_stamp,
                                             artifact_time_stamp=self.config.time_stamp,
                                             running_status=False,
                                             start_time=Pipeline.experiment.start_time,
                                             stop_time=stop_time,
                                             execution_time=stop_time - Pipeline.experiment.start_time,
                                             message="Pipeline has been completed.",
                                             experiment_file_path=Pipeline.experiment_file_path,
                                             is_model_accepted=model_evaluation_artifact.is_model_accepted,
                                             accuracy=model_trainer_artifact.model_accuracy
                                             )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()
            
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
        
    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
        
        
    def save_experiment(self):
        try:
            if Pipeline.experiment.experiment_id is not None:
                experiment = Pipeline.experiment
                experiment_dict = experiment._asdict()
                experiment_dict: dict = {key: [value] for key, value in experiment_dict.items()}

                experiment_dict.update({
                    "created_time_stamp": [datetime.now()],
                    "experiment_file_path": [os.path.basename(Pipeline.experiment.experiment_file_path)]})
                
                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path), exist_ok=True)
                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path, index=False, header=False, mode="a")
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path, mode="w", index=False, header=True)
            else:
                print("First start experiment")
                
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
        
    @classmethod
    def get_experiments_status(cls, limit: int = 5) -> pd.DataFrame:
        try:
            if os.path.exists(Pipeline.experiment_file_path):
                df = pd.read_csv(Pipeline.experiment_file_path)
                limit = -1 * int(limit)
                return df[limit:].drop(columns=["experiment_file_path", "initialization_timestamp"], axis=1)
            else:
                return pd.DataFrame()
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
        