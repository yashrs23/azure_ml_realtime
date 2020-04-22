from locust import HttpLocust, TaskSet, task
import os
import pandas as pd
from utilities import text_to_json
from itertools import cycle

_NUMBER_OF_REQUESTS = os.getenv('NUMBER_OF_REQUESTS', 100)
dupes_test_path = './data_folder/dupes_test.tsv'
dupes_test = pd.read_csv(dupes_test_path, sep='\t', encoding='latin1')
dupes_to_score = dupes_test.iloc[:_NUMBER_OF_REQUESTS, 4]
_SCORE_PATH = os.getenv('SCORE_PATH', "/score")
_API_KEY = os.getenv('API_KEY')


class UserBehavior(TaskSet):
    def on_start(self):
        print('Running setup')
        self._text_generator = cycle(dupes_to_score.apply(text_to_json))
        self._headers = {
            "content-type": "application/json",
            'Authorization': ('Bearer {}'.format(_API_KEY))
        }

    @task
    def score(self):
        self.client.post(_SCORE_PATH,
                         data=next(self._text_generator),
                         headers=self._headers)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    # min and max time to wait before repeating task
    min_wait = 10
    max_wait = 200
