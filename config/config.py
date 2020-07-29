import sched
import time

import pyodbc
import requests
import yaml


class AppConfig:
    def __init__(self):
        self.config = None
        self._load()

    def _load(self):
        with requests.get('https://codeday.blob.core.windows.net/codeday-ml-ci-cd/resources/config.yaml') as res:
            self.config = yaml.safe_load(res.text)

    def _schedule(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(5 * 60, 1, self._load)
        scheduler.run()


class DBConfig:
    def __init__(self):
        self.app_config = AppConfig()

    def get_connection(self):
        conn_string = 'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{url};Database=codeday;Uid={user};' \
                      'Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        url = self.app_config.config['db']['url']
        user = self.app_config.config['db']['user']
        password = self.app_config.config['db']['password']

        connection = pyodbc.connect(
            conn_string.format(
                url=url,
                user=user,
                password=password
            )
        )
        return connection
