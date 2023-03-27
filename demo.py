from housing.pipeline.pipeline import Pipeline
from housing.logger.logger import logging
from housing.exception.exception import HousingException
import sys

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    try:
        pipe=Pipeline()
        pipe.run_pipeline()
    except Exception as e:
            logging.error(f"Error Occured at {HousingException(e,sys)}")
            raise HousingException(e,sys) from e 




if __name__=='__main__':
    main()