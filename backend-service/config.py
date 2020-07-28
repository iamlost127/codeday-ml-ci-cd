import os
import sched
import time

import yaml


class AppConfig:
    def __init__(self):
        self.config_path = os.getenv('CONFIG_PATH', 'resources/config.yml')
        self.config = None
        self._load()

    def _load(self):
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)

    def _schedule(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(5 * 60, 1, self._load)
        scheduler.run()

    def __call__(self):
        return self.config
