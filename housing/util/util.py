import os
import sys
import yaml


from housing.exception.exception import HousingException
from housing.logger.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """
    Read YAML file and Returns A Content as Dictionary.
    File path : str
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        logging.info(f"Error Occured at {HousingException(e,sys)}")
        raise HousingException(e, sys)




    try:
        pass
    except Exception as e:
        logging.info(f"Error Occured at {HousingException(e,sys)}")
        raise HousingException(e, sys)