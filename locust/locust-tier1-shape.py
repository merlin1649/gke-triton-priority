import time
from locust import HttpUser, task, between
import json
import math

# class CustomLoad(locust.LoadTestShape):
#     """
#     The load shape class that progressively adds users up to the maximum.
#     After the maximum load has been reached the class starts to progressively decrease 
#     the load till all users are stopped.
#     """

#     max_steps = 11
#     step_time = 60
#     step_load = 2
#     spawn_rate = 10

#     def tick(self):
#         run_time = self.get_run_time()

#         current_step = math.floor(run_time / self.step_time) + 1

#         if current_step <= self.max_steps:
#             return (current_step * self.step_load, self.spawn_rate)
#         else:
#             return None

class DoubleWave(LoadTestShape):
    """
    A shape to immitate some specific user behaviour. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3
    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 20
    peak_one_users = 200
    peak_two_users = 200
    time_limit = 200

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                (self.peak_one_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                + (self.peak_two_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                + self.min_users
            )
            return (round(user_count), round(user_count))
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

