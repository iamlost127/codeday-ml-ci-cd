import os

import numpy as np

from flask import Flask, request, jsonify, Response
from joblib import load


class ModelLoader:
    def __init__(self):
        all_versions = [int(x.split('.')[1][1:]) for x in os.listdir('models')]
        latest = max(all_versions)
        self.all_models = dict()
        self.latest_version = 'v' + str(latest)

        for f in os.listdir('models'):
            self.all_models[f.split('.')[1]] = load('models/' + f)


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
