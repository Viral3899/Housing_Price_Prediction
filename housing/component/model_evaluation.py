import os
import sys
import pandas as pd


from housing.config.configuration import Configuration
from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.constant import *
from housing.util.util import read_yaml_file, load_data, load_numpy_array_data, load_object, write_yaml_file
from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from housing.entity.model_factory import evaluate_regression_model


class ModelEvaluation:

    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact) -> None:

        try:
            logging.info(
                f"\n\n{'='*20} Model Evaluation log Started {'='*20}\n\n")
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_best_model(self,):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path)
                return model

            model_evaluation_file_content = read_yaml_file(
                file_path=model_evaluation_file_path)
            model_evaluation_file_content = dict(
            ) if model_evaluation_file_content is None else model_evaluation_file_content

            if BEST_MODEL_KEY not in model_evaluation_file_content:
                return model

            model = load_object(
                file_path=model_evaluation_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def update_evaluation_report(self,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]
                
            logging.info(f'Previous Eval Results : {model_eval_content}')
            
            eval_result = {
                BEST_MODEL_KEY : {
                    MODEL_PATH_KEY : model_evaluation_artifact.evaluated_model_path
                }
            }
            
            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp : previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY : model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)
            
            model_eval_content.update(eval_result)
            logging.info(f'update Eval Results : {model_eval_content}')
            write_yaml_file(file_path=eval_file_path
                            ,data=model_eval_content)
            
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)
            train_file_path =  self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            schema_file_path = self.data_validation_artifact.schema_file_path
            
            logging.info('Loading data for model evaluation')
            train_dataframe = load_data(file_path=train_file_path,
                                        schema_file_path=schema_file_path
                                        )
            test_dataframe = load_data(file_path=test_file_path,
                                       schema_file_path=schema_file_path
                                        )
            
            schema_content = read_yaml_file(file_path=schema_file_path)
            
            target_column = schema_content[TARGET_COLUMN_KEY]
            logging.info("Splitting Data into target and features")
            train_target = train_dataframe[target_column]
            test_target = test_dataframe[target_column]
            
            train_dataframe = train_dataframe.drop(target_column,axis=1,inplace=True)
            test_dataframe = test_dataframe.drop(target_column,axis=1,inplace=True)
            
            logging.info("All set for Evaluation")
            
            model = self.get_best_model()
            
            if model is None:
                logging.info("No Existing Model Found Hence Accepting Trained Model")
                model_evaluation_artifact =ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                   is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted model evaluation artifact{model_evaluation_artifact} created successfully")
                return model_evaluation_artifact
            
            model_list = [model, trained_model_object]
            print(model_list)
            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                    X_train=train_dataframe,
                                                    y_train=train_target,
                                                    X_test=test_dataframe,
                                                    y_test=test_target,
                                                    base_accuracy=self.model_trainer_artifact.model_accuracy
                                                    )
            logging.info(f'model Evaluation Completed model metric info artifact : {metric_info_artifact}')
            
            if metric_info_artifact is None:
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=False,
                                                  evaluated_model_path=trained_model_file_path
                                                  )
                logging.info(model_evaluation_artifact)
                
                return model_evaluation_artifact
            
            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True
                                                                    )
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f'Model Accepted , Model Evaluation Artifact {model_evaluation_artifact}')

            else:
                logging.info('Trained Model is not Better Than Existing Model hence Not Accepting Trained Model')
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=False
                                                                    )
                return model_evaluation_artifact
                      
        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)
    
    def __del__(self):
        logging.info(
            f"\n\n{'='*20} Model Evaluation Log Completed {'='*20} \n\n")