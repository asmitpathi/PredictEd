import os
import sys
from src.exception import CustomException 
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:     # stores configuration values
    train_data_path: str= os.path.join('artifacts', 'train.csv')    # str is the type hint
    test_data_path: str= os.path.join('artifacts', 'test.csv')      # artifacts folder
    raw_data_path: str= os.path.join('artifacts', 'data.csv')

class DataIngestion:     # here @dataclass is not used because some functions are also defined inside it
    def __init__(self):
        self.ingestion_config= DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df= pd.read_csv('notebook/data/stud.csv')    # read the dataset
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok= True)   # create artifacts folder,  exist_ok=True means if it is already there, we will keep the folder instead of deleting it and creating it again or returning any error

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header= True)   # save a copy of the original dataset

            logging.info('Train test split initiated')
            train_set, test_set= train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header= True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header= True)

            logging.info('Ingestion of data is completed')

            return(    # both are required for data transformation
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path    
            )
        except Exception as e:
            raise CustomException(e, sys)