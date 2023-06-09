import os
import sys
import pandas as pd
import numpy as np


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


from housing.constant import *
from housing.exception.exception import HousingException
from housing.logger.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig
from housing.config.configuration import Configuration
from housing.util.util import read_yaml_file, load_data, save_numpy_array_data, save_object


class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(self, add_bedrooms_per_room=True,
                 total_rooms_ix=3,
                 population_ix=5,
                 households_ix=6,
                 total_bedrooms_ix=4, columns=None):
        """
        FeatureGenerator Initialization
        add_bedrooms_per_room: bool
        total_rooms_ix: int index number of total rooms columns
        population_ix: int index number of total population columns
        households_ix: int index number of  households columns
        total_bedrooms_ix: int index number of bedrooms columns
        """
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def fit(self, X, y=None):
        """
        The fit function is used to fit the data into the model

        :param X: A numpy array or sparse matrix of shape [n_samples, n_features]
        :param y: the target variable
        :return: The fit method returns the instance of the class.
        """
        return self

    def transform(self, X, y=None):
        """
        It takes the total number of rooms in a district, divides it by the number of households, and
        adds this value to the data as a new attribute

        :param X: The input data
        :param y: The target variable
        :return: The generated feature is being returned.
        """
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                X[:, self.households_ix]

            population_per_household = X[:,
                                         self.population_ix] / X[:, self.households_ix]

            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                    X[:, self.total_rooms_ix]

                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]

            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)


class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact
                 ):
        """
        The function takes in three arguments: data_transformation_config, data_ingestion_artifact,
        data_validation_artifact

        :param data_transformation_config: This is a class that contains the configuration for the data
        transformation
        :type data_transformation_config: DataTransformationConfig
        :param data_ingestion_artifact: This is the output of the data ingestion step. It contains the
        dataframe that was created in the data ingestion step
        :type data_ingestion_artifact: DataIngestionArtifact
        :param data_validation_artifact: This is the output of the data validation step
        :type data_validation_artifact: DataValidationArtifact
        """

        try:
            logging.info(
                f"\n\n{'='*20} Data Transformation log Started {'='*20}\n\n")

            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def get_data_transformer_object(self) -> ColumnTransformer:
        """
        It takes the schema file path as input and returns a ColumnTransformer object which is used to
        transform the data
        :return: A ColumnTransformer object
        """
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path

            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            num_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='median')),
                ('feature_generator', FeatureGenerator(
                    add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                    columns=numerical_columns
                )),
                ('scaler', StandardScaler())

            ])

            cat_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder()),
                ('scaler', StandardScaler(with_mean=False))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessing = ColumnTransformer(transformers=[
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns)
            ])

            return preprocessing

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        It takes the training and testing dataframe, splits the input and target feature, applies the
        preprocessing object on the input feature, and saves the transformed training and testing array
        and preprocessing object.
        :return: DataTransformationArtifact
        """
        try:
            logging.info('Obtaining preprocessing Object')

            preprocessing_obj = self.get_data_transformer_object()

            logging.info('Getting Train and Test File Path')
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            logging.info(
                'Loading Training And Testing File As Panda DataFrame')

            train_df = load_data(file_path=train_file_path,
                                 schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path,
                                schema_file_path=schema_file_path)

            dataset_schema = read_yaml_file(schema_file_path)
            target_column_name = dataset_schema[TARGET_COLUMN_KEY]

            logging.info(
                f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(
                columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(
                columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr = preprocessing_obj.fit_transform(
                input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(
                input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,
                              np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr,
                             np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(
                train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(
                test_file_path).replace(".csv", ".npz")

            transformed_train_file_path = os.path.join(
                transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(
                transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            save_numpy_array_data(
                file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(
                file_path=transformed_test_file_path, array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path,
                        obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
                                                                      message="Data transformation successful.",
                                                                      transformed_train_file_path=transformed_train_file_path,
                                                                      transformed_test_file_path=transformed_test_file_path,
                                                                      preprocessed_object_file_path=preprocessing_obj_file_path

                                                                      )
            logging.info(
                f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            logging.info(f"Error Occurred at {HousingException(e,sys)}")
            raise HousingException(e, sys)

    def __del__(self):

        logging.info(
            f"\n\n{'='*20} Data Transformation Log Completed {'='*20} \n\n")
