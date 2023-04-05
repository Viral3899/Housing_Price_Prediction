from housing.pipeline.pipeline import Pipeline
from housing.logger.logger import logging
from housing.exception.exception import HousingException
from housing.config.configuration import Configuration
import sys

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    try:
        pipe = Pipeline()
        pipe.run()

    except Exception as e:
        logging.error(f"Error Occurred at {HousingException(e,sys)}")
        raise HousingException(e, sys)


if __name__ == '__main__':
    main()
