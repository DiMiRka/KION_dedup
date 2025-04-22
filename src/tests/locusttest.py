import json
import random
import logging

from locust import HttpUser, task, between
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


class APIdedup(HttpUser):
    host = "http://0.0.0.0:8000"
    wait_time = between(0.1, 0.5)

    def on_start(self):
        with open("src/tests/test_data.json", "r", encoding="utf-8") as file:
            self.test_data = json.load(file)

    @task
    def post_event(self):
        try:
            data_event = random.choice(self.test_data)
            with self.client.post("/events/event_post/",
                                  json=data_event,
                                  headers={"Content-Type": "application/json"},
                                  timeout=30,
                                  catch_response=True) as response:
                if response.status_code == 0:
                    response.failure("No response from server (status 0)")
                elif response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
