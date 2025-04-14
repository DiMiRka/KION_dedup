from locust import HttpUser, TaskSet, task, between
import json
from dotenv import load_dotenv
from sqlalchemy import null, false

load_dotenv()


class EvenPostTest(TaskSet):
    pass


class APIdedup(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task
    def post_event(self):
        with open("src/tests/testlocust.json", "r") as file:
            data_event = file.read()

        with self.client.post("/events/event_post/", data=data_event, catch_response=True) as response:
            if response.status_code == 200:
                return response.success
            else:
                response.failure(f'status code is {response.status_code}')

