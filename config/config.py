import logging
import sched
import time

import pyodbc
import requests
import yaml

LOGGER = logging.getLogger(__name__)


class AppConfig:
    def __init__(self):
        self.config = None
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self._load()
        self.scheduler.run()

    def _load(self):
        with requests.get('https://codeday.blob.core.windows.net/codeday-ml-ci-cd/resources/config.yaml') as res:
            self.config = yaml.safe_load(res.text)
        self.scheduler.enter(60, 1, self._load)
        LOGGER.debug('loaded latest application configuration')


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
