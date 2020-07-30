import logging
import os
import sched
import threading
import time
import xml.etree.ElementTree as ET

import numpy as np
import requests

from flask import Flask, request, jsonify, Response
from joblib import load

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
LOGGER = logging.getLogger(__name__)


class ModelLoader:

    AZURE_MODEL_CONTAINER = 'https://codeday.blob.core.windows.net/codeday-ml-ci-cd'

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.all_models = dict()
        self._load_models()
        schedule_thread = threading.Thread(target=self.scheduler.run)
        schedule_thread.start()

    def _load_models(self):
        LOGGER.info('looking for new models in Azure blob storage')
        model_list_url = ModelLoader.AZURE_MODEL_CONTAINER + '?restype=container&comp=list&prefix=models'
        model_list_res = requests.get(model_list_url)

        root = ET.fromstring(model_list_res.text)
        all_models = [blob.find('Name').text for blob in root.find('.').find('Blobs').findall('Blob')]
        all_versions = [int(x.split('.')[1][1:]) for x in all_models]
        latest = max(all_versions)

        self.latest_version = 'v' + str(latest)

        for m in all_models:
            model_name = m.split('.')[1]

            if model_name in self.all_models:
                continue

            LOGGER.info('Found new model: {}, updating model dict'.format(m))
            url = ModelLoader.AZURE_MODEL_CONTAINER + '/' + m
            res = requests.get(url)
            with open('model.tmp', 'wb') as f:
                f.write(res.content)

            mo = load('model.tmp')
            os.remove('model.tmp')
            self.all_models[model_name] = mo

        self.scheduler.enter(30, 1, self._load_models)


model_loader = ModelLoader()

app = Flask(__name__)


def _predict(pred_json, model):
    x_pred = np.zeros((1, 7))
    x_pred[0, 0] = pred_json['gre_score']
    x_pred[0, 1] = pred_json['toefl_score']
    x_pred[0, 2] = pred_json['ug_univ_rating']
    x_pred[0, 3] = pred_json['sop_score']
    x_pred[0, 4] = pred_json['lor_score']
    x_pred[0, 5] = pred_json['gpa']
    x_pred[0, 6] = pred_json['research']

    pred = model.predict(x_pred)
    pred = int(np.squeeze(pred))
    pred_prob = model.predict_proba(x_pred)
    confidence_score = float(pred_prob[0, pred])
    return pred, confidence_score


@app.route('/version', methods=['GET'])
def model_version():
    return jsonify({'latest': model_loader.latest_version})


@app.route('/predict/', methods=['POST'])
def predict_latest():
    pred_json = request.get_json(silent=True)
    model = model_loader.all_models[model_loader.latest_version]
    pred, confidence_score = _predict(pred_json, model)
    return jsonify({
        'result': pred,
        'confidence_score': confidence_score,
        'model_version': model_loader.latest_version
    })


@app.route('/<string:version>/predict/', methods=['POST'])
def predict_version(version):
    pred_json = request.get_json(silent=True)
    if version not in model_loader.all_models:
        return Response('{"error": "wrong model version"}', content_type='application/json', status=400)

    model = model_loader.all_models[version]
    pred, confidence_score = _predict(pred_json, model)
    return jsonify({
        'result': pred,
        'confidence_score': confidence_score,
        'model_version': version
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
