import os
import sys
import yaml
import pandas as pd
import numpy as np
import dill


from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.constant import *

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


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        dataset_schema= read_yaml_file(schema_file_path)

        schema=dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe= pd.read_csv(file_path)

        error_message =  ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column] = dataframe[column].astype(schema[column])
            else:
                error_message = f'{error_message} \nColumn {column} is not in the schema'
        if len(error_message)>0:
            raise Exception(error_message)
        return dataframe



    except Exception as e:
        logging.info(f"Error Occured at {HousingException(e,sys)}")
        raise HousingException(e, sys) from e
    




def save_numpy_array_data(file_path : str,  array : np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path, 'wb') as file_obj:
            np.save(file=file_obj,arr=array)

    except Exception as e:
        logging.info(f"Error Occured at {HousingException(e,sys)}")
        raise HousingException(e, sys) from e


def save_object(file_path:str,obj):


    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path, 'wb') as file_obj:
            dill.dump(file=file_obj,obj=obj)

    except Exception as e:  
        logging.info(f"Error Occured at {HousingException(e,sys)}")
        raise HousingException(e, sys) from e
    

    


    
































