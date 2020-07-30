import logging
import os

import xml.etree.ElementTree as ET

import pandas as pd
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from config import AppConfig, DBConfig
from joblib import dump


LOGGER = logging.getLogger(__name__)


class ModelTraining:

    AZURE_MODEL_CONTAINER = 'https://codeday.blob.core.windows.net/codeday-ml-ci-cd'

    def __init__(self):
        self.app_config = AppConfig()
        self.db_config = DBConfig()

    def train(self):
        LOGGER.info('Started model training..')
        connection = self.db_config.get_connection()
        with connection.cursor() as _:
            data = pd.read_sql('select * from grad_admission', con=connection)

            labels = data['admit']
            features = data.drop(columns='admit')

            x_train, x_val, y_train, y_val = train_test_split(features, labels, test_size=0.25, random_state=42)

            max_iter = self.app_config.config['model']['train']['hyperparams']['max_iter']

            model = LogisticRegression(max_iter=max_iter)
            model = model.fit(x_train, y_train)
            val_score = model.score(x_val, y_val)

            logging.info('Model trained, val score: {}'.format(val_score))
            return model, val_score

    def evaluate_model(self, val_score):
        eval_threshold = self.app_config.config['model']['train']['eval_threshold']
        return val_score > eval_threshold

    def save_model(self, model):
        model_list_url = ModelTraining.AZURE_MODEL_CONTAINER + '?restype=container&comp=list&prefix=models'
        model_list_res = requests.get(model_list_url)

        root = ET.fromstring(model_list_res.text)
        all_models = [blob.find('Name').text for blob in root.find('.').find('Blobs').findall('Blob')]
        all_versions = [int(x.split('.')[1][1:]) for x in all_models]
        latest_version = max(all_versions)

        new_version_num = latest_version + 1
        saved_model_path = 'model.v' + str(new_version_num)
        dump(model, saved_model_path)
        return os.path.abspath(saved_model_path)
