import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessing_obj_file_path: str= os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config= DataTransformationConfig()
    
    def get_data_transformation_object(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]      # define the numerical columns
            categorical_columns = [                                   
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]             # define the categorical columns

            logging.info(f"Numerical Columns: {numerical_columns} & Categorical Columns: {categorical_columns}")
            
            num_pipeline= Pipeline(       # numerical columns
                steps= [
                    ('imputer', SimpleImputer(strategy='median')),        # handling missing values
                    ('scaler', StandardScaler())          # feature scaling
                ]
            )

            cat_pipeline= Pipeline(       # categorical columns
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),     # handling missing values
                    ('one_hot_encoder', OneHotEncoder()),        # encoding categorical columns
                    ('scaler', StandardScaler(with_mean=False))          # feature scaling
                ]
            )

            preprocessor= ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info("Reading training and testing data")
            train_df= pd.read_csv(train_path)
            test_df= pd.read_csv(test_path)

            logging.info("Obtaining preprocessing object")
            preprocessing_obj= self.get_data_transformation_object()

            target_column_name="math_score"

            logging.info("Splitting training and testing data into features and labels")
            input_feature_train_df= train_df.drop([target_column_name], axis=1)
            target_label_train_df= train_df[target_column_name]
            input_feature_test_df= test_df.drop([target_column_name], axis=1)
            target_label_test_df= test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframe")
            input_feature_train_arr= preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr= preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_label_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_label_test_df)]

            logging.info("Saving preprocessing object")
            save_object(
                file_path= self.data_transformation_config.preprocessing_obj_file_path,
                obj= preprocessing_obj
                )
            
            logging.info('Transformation of data is completed')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessing_obj_file_path,
            )
        
        except Exception as e:
            raise CustomException(e,sys)