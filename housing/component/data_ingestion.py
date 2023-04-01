import os
import sys
import requests
from six.moves import urllib
import tarfile
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedShuffleSplit

from housing.logger.logger import logging
from housing.exception.exception import HousingException

from housing.entity.config_entity import DataIngestionConfig
from housing.config.configuration import Configuration
from housing.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(
                f"\n\n{'='*20} Data Ingestion log Started {'='*20}\n\n")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def download_housing_data(self,) -> str:
        """
        It downloads the housing data from the remote url and stores it in the local file system
        :return: The file path of the downloaded file.
        """
        try:
            # extraction remote url to download url
            download_url = self.data_ingestion_config.dataset_download_url

            # folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            os.makedirs(tgz_download_dir, exist_ok=True)

            housing_file_name = os.path.basename(download_url)

            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            logging.info(f"""
             --> Started Downloading......
             --> From URL : [{download_url}]
             --> Into Folder : [{tgz_file_path}]
             """)

            urllib.request.urlretrieve(download_url, tgz_file_path)

            # response = requests.get(download_url)
            # with open(tgz_file_path, 'wb') as f:
            #     f.write(response.content)

            logging.info(
                f"File :[{tgz_file_path}] has been downloaded successfully.")

            return tgz_file_path

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def extract_tgz_file(self, tgz_file_path: str):
        """
        It extracts the contents of a tgz file to a directory
        
        :param tgz_file_path: The path to the tgz file that you want to extract
        :type tgz_file_path: str
        """
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            logging.info(f"""
            --> Extracting Data from tgz file :  [{tgz_file_path}]
            --> to raw data dir : [{raw_data_dir}]
            """)

            os.makedirs(raw_data_dir, exist_ok=True)

            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def split_data_as_train_test(self,) -> DataIngestionArtifact:
        """
        It reads the data from the raw data directory, splits the data into train and test, and writes
        the train and test data into the ingested train and test directories
        :return: DataIngestionArtifact
        """
        try:

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            housing_file_path = os.path.join(raw_data_dir, file_name)

            housing_data_frame = pd.read_csv(housing_file_path)

            logging.info(f'Reading file data from [{housing_file_path}]')
            housing_data_frame['income_category'] = pd.cut(
                housing_data_frame['median_income'],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1, 2, 3, 4, 5]
            )

            logging.info(f'Splitting Data into Train Test')
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(
                n_splits=1, test_size=0.2, random_state=0)

            for train_index, test_index in split.split(housing_data_frame, housing_data_frame["income_category"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(
                    ["income_category"], axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(
                    ["income_category"], axis=1)

            train_file_path = os.path.join(
                self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(
                self.data_ingestion_config.ingested_test_dir, file_name)

            if strat_train_set is not None:
                os.makedirs(
                    self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(
                    f'Exporting training Dataset into [{train_file_path}]')
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(
                    self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(
                    f'Exporting testing Dataset into [{test_file_path}]')
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data Ingestion Completed Successefully")

            logging.info(
                f'Data Ingestion Artifact : [{data_ingestion_artifact}]')

            return data_ingestion_artifact

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def initiate_data_ingestion(self,) -> DataIngestionArtifact:
        """
        It downloads the housing data, extracts the tgz file, and splits the data into train and test
        sets
        :return: DataIngestionArtifact
        """
        try:
            tgz_file_path = self.download_housing_data()

            self.extract_tgz_file(tgz_file_path=tgz_file_path)

            return self.split_data_as_train_test()

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def __del__(self):

        logging.info(
            f"\n\n{'='*20} Data Ingestion Log Completed {'='*20} \n\n")
