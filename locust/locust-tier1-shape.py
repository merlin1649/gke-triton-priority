import time
from locust import HttpUser, task, between
from locust import LoadTestShape
import json
from math import sin, pi

class SineLoad(LoadTestShape):
    """
    """

    target_users   = 600
    step_users     = 5      # ramp users each step
    sine_amplitude = 5      # percent
    sine_period    = 20     # seconds
    time_limit     = 3600   # seconds

    def tick(self):
        num_steps = self.target_users/self.step_users
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            if num_steps < run_time:
                user_count = num_steps * self.step_users
            else:
                user_count = self.target_users
            # theta = 2*pi*(run_time % self.sine_period)/self.sine_period
            # user_count = min(
            #     round(self.target_users*(sin(theta)*self.sine_amplitude/100 + 1)),
            #     self.step_users*run_time
            # )
            return (user_count,self.step_users)
        else:
            return None

class TritonUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def bert_tier1(self):
        response = self.client.post(self.url1, headers=self.headers, data=json.dumps(self.data))

    @task
    def bert_tier1(self):
        response = self.client.post(self.url1, data=json.dumps(self.data))
    

    def on_start(self):
        with open('bert_request.json') as f:
            self.data = json.load(f)

        self.url1 = '{}/v2/models/{}/infer'.format(
            self.environment.host,
            'bert-tier1')

        self.headers = {'Connection': 'close'}

