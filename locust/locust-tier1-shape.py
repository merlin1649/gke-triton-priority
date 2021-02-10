import time
from locust import HttpUser, task, between
from locust import LoadTestShape
import json
from math import sin, pi

class SineLoad(LoadTestShape):
    """
    """

    target_users   = 400
    sine_amplitude = 5      # percent
    sine_period    = 20     # seconds
    time_limit     = 1200   # seconds

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            theta = 2*pi*(run_time % self.sine_period)/self.sine_period
            user_count = round(self.target_users*(sin(theta)*self.sine_amplitude/100 + 1))
            return (user_count,user_count)
        else:
            return None

class TritonUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def bert_tier1(self):
        response =self.client.post(self.url1, data=json.dumps(self.data))

    def on_start(self):
        with open('bert_request.json') as f:
            self.data = json.load(f)

        self.url1 = '{}/v2/models/{}/infer'.format(
            self.environment.host,
            'bert-tier1')

