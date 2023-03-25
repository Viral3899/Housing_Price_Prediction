import os
from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"


ROOT_DIR=os.getcwd()  # to get Current Working Directory
CONFIG_DIR='config'
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#Training Pipeline Config Constants

TRAINING_PIPELINE_CONFIG_KEY='training_pipeline_config'
TRAINING_PIPELINE_NAME_KEY='pipeline_name'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY='artifact_dir'


#Data Ingestion Pipeline Config Constants
DATA_INGESTION_ARTIFACT_DIR='data_ingestion'
DATA_INGESTION_CONFIG_KEY='data_ingestion_config'
DATA_INGESTION_DOWNLOAD_URL_KEY='dataset_download_url'
DATA_INGESTION_RAW_DATA_DIR_KEY ='raw_data_dir'
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY='tgz_download_dir'
DATA_INGESTION_INGESTED_DIR_KEY="ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY="ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY="ingested_test_dir"












