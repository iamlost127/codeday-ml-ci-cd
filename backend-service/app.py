import json
import requests

from flask import Flask, request, Response
from jsonschema import validate, exceptions

from config import AppConfig

app = Flask(__name__)


def _load_schema():
    with open('resources/schema.json') as s:
        return json.load(s)


SCHEMA = _load_schema()
config = AppConfig()()


@app.route('/admit', methods=['POST'])
def admit_prod():
    data = request.get_json()
    try:
        validate(instance=data, schema=SCHEMA)
        url = config['model']['url']
        version = config['model']['version']

        url = url + '/predict' if version == 'latest' else url + '/' + version + '/predict'
        response = requests.post(url=url, json=data)
        return response.json()

    except exceptions.ValidationError:
        return Response('{"error": "Invalid input json"}', content_type='application/json', status=401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
