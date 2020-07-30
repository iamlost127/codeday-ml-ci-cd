import time

import requests

import os
import subprocess


os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_RUN_PORT'] = '5000'
subprocess.Popen(['flask', 'run'])
time.sleep(5)


def test():
    res = requests.get('http://localhost:5000/version')
    assert res.status_code == 200
