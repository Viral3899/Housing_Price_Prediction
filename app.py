import sys
import os

from flask import Flask, request, render_template
from housing.exception.exception import HousingException
from housing.logger.logger import logging

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        raise Exception("Exception Testing")
    except Exception as e:
        housing = HousingException(e, sys)
        logging.info(housing.error_message)

    return """
    <h1>Start Machine Learning Project</h1>
    """


if __name__ == '__main__':
    app.run(debug=True)
