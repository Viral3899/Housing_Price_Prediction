import os
import numpy as np
import threading
from flask import Flask, render_template, request
import joblib
from housing.pipeline.pipeline import Pipeline
from housing.entity.housing_predictor import HousingData, HousingPredictor
from housing.config.configuration import Configuration
from housing.constant import *

app = Flask(__name__)

# Load the pipeline for retraining the model


ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "housing"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
HOUSING_DATA_KEY = "housing_data"
MEDIAN_HOUSING_VALUE_KEY = "median_house_value"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        housing_median_age = float(request.form['housing_median_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        median_income = float(request.form['median_income'])
        ocean_proximity = request.form['ocean_proximity']

        housing_data = HousingData(longitude=longitude,
                                   latitude=latitude,
                                   housing_median_age=housing_median_age,
                                   total_rooms=total_rooms,
                                   total_bedrooms=total_bedrooms,
                                   population=population,
                                   households=households,
                                   median_income=median_income,
                                   ocean_proximity=ocean_proximity)
        housing_df = housing_data.get_housing_input_data_frame()
        housing_predictor = HousingPredictor(model_dir=MODEL_DIR)
        prediction = housing_predictor.predict(X=housing_df)

        prediction_str = f"${prediction[0]:,.2f}"
        # Render the template with the prediction result
        return render_template('result.html', longitude=longitude, latitude=latitude,
                               housing_median_age=housing_median_age, total_rooms=total_rooms,
                               total_bedrooms=total_bedrooms, population=population, households=households,
                               median_income=median_income,
                               ocean_proximity=ocean_proximity, prediction=prediction_str)

    # Render the template with the input form
    return render_template('index.html')


@app.route('/retrain', methods=['GET', 'POST'])
def retrain():
    message = ""
    pipeline = Pipeline(config=Configuration(
        current_time_stamp=get_current_time_stamp()))
    if Pipeline.experiment.running_status == False and Pipeline.experiment.stop_time != np.nan:
        message = "Training is completed."
    if request.method == 'POST':
        if not Pipeline.experiment.running_status:
            message = "Re-Training started."
            pipeline.start()
        else:
            message = "Training is already in progress."

    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('retrain.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
