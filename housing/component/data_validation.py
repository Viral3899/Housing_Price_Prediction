import sys
import os
import pandas as pd
import numpy as np
from collections import Counter
import json

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab


from housing.logger.logger import logging
from housing.exception.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.util.util import read_yaml_file
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.config.configuration import Configuration


class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig,

                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(
                f"\n\n{'='*20} Data Validation log Started {'='*20}\n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(
                self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
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

            if not is_availabel:
                message = f'Training File : [{train_file_path}] or\n Testing File : [{test_file_path}] is not present.'
                logging.info(message)
                raise Exception(message)

            return is_availabel

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def validate_dataset_schema(self) -> bool:
        try:
            is_schema_validated = False

            schema_file_path = self.data_validation_config.schema_file_path
            schema_config = read_yaml_file(file_path=schema_file_path)

            train_df, test_df = self.get_train_and_test_df()
            train_df_columns = train_df.columns
            test_df_columns = test_df.columns

            logging.info('Validating Number of Colums')
            number_of_cols_validate = False
            if (len((schema_config['columns'].keys())) == (len(train_df_columns)-1)) & (len((schema_config['columns'].keys())) == (len(test_df_columns)-1)):
                number_of_cols_validate = True
                logging.info('Number of cols are Validated')

            logging.info(f'Checking weather target Columns is Avlilable]')
            is_target_column_avilable = False
            if (schema_config['target_column'] in train_df_columns) and (schema_config['target_column'] in test_df_columns):
                is_target_column_avilable = True
                logging.info(
                    f'Target Column is Available [{schema_config["target_column"]}]')

            logging.info(
                f'Validating Datatype of Columns with Given Schema at [{schema_file_path}]')
            data_type_of_cols_validate = False
            if (Counter(schema_config['numerical_columns'])) == (Counter([col for col in train_df.columns if train_df[col].dtype != 'O'])) \
                    and (Counter(schema_config['numerical_columns'])) == (Counter([col for col in test_df.columns if test_df[col].dtype != 'O'])) \
                    and (Counter(schema_config['categorical_columns'])) == (Counter([col for col in train_df.columns if test_df[col].dtype == 'O'])) \
                    and (Counter(schema_config['categorical_columns'])) == (Counter([col for col in test_df.columns if test_df[col].dtype == 'O'])):
                data_type_of_cols_validate = True
                logging.info(
                    'DataType of Columns are passed Successfully for both Data')

            logging.info(
                f'Validating Domain Values of Columns with Given Schema at [{schema_file_path}]')
            is_domain_value_validate = False
            if Counter(schema_config['domain_value']['ocean_proximity']) == Counter(train_df['ocean_proximity'].unique()) == Counter(test_df['ocean_proximity'].unique()):
                is_domain_value_validate = True
                logging.info(
                    f'Domain values of Columns [{list(schema_config["domain_value"].keys())}] are passed Successfully for both Data')
            is_schema_validated = number_of_cols_validate and is_domain_value_validate and is_target_column_avilable and data_type_of_cols_validate

            if not is_schema_validated:
                message = f"Either Number of Columns or Datatype of Columns or Domain VAlues of Column  is Not Matched "
                logging.info(message)
                raise Exception(message)

            return is_schema_validated

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.get_train_and_test_df()
            profile.calculate(train_df, test_df)
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(self.data_validation_config.report_file_path, "w") as report_file:
                json.dump(report, report_file)

            return report

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df, test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)

            dashboard.save(self.data_validation_config.report_page_file_path)

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def is_data_drift_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()

            return True
        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path,
                                                              report_file_path=self.data_validation_config.report_file_path,
                                                              report_page_file_path=self.data_validation_config.report_page_file_path,
                                                              is_validated=True,
                                                              message='Data validation performed successfully')
            logging.info(
                f"Data VAlidation Artifact: [{data_validation_artifact}]")

        except Exception as e:
            logging.info(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e, sys) from e


    def __del__(self):

        logging.info(
            f"\n\n{'='*20} Data Validation Log Completed {'='*20} \n\n")
