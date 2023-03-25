import os
from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"


ROOT_DIR=os.getcwd()  # to get Current Working Directory
CONFIG_DIR='config'
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#Taining Pipeline Config Constants

TRAINING_PIPELINE_CONFIG_KEY='training_pipeline_config'
TRAINING_PIPELINE_NAME_KEY='pipeline_name'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY='artifact_dir'











