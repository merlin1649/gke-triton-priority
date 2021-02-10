import time
from locust import HttpUser, task, between
import json

class QuickstartUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def bert_tier2(self):
        response =self.client.post(self.url2, data=json.dumps(self.data))

    def on_start(self):
        with open('bert_request.json') as f:
            self.data = json.load(f)

        self.url2 = '{}/v2/models/{}/infer'.format(
            self.environment.host,
            'bert-tier2')

        self.headers = {'Content-Type': 'application/json'}
