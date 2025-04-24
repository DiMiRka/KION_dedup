import json
import random
import logging

from locust import HttpUser, task, between
from dotenv import load_dotenv
from typing import Dict, Any
from multiprocessing import Lock

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


class APIdedup(HttpUser):
    host = "http://0.0.0.0:8000"
    wait_time = between(0.1, 0.5)
    connection_timeout = 10.0
    network_timeout = 30.0
    _shared_test_data = None
    _failure_cache: Dict[str, int] = {}
    _data_lock = Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if APIdedup._shared_test_data is None:
            APIdedup._shared_test_data = self._load_test_data()
        self.test_data = APIdedup._shared_test_data

    @staticmethod
    def _load_test_data() -> list[Any]:
        with open("src/tests/test_data.json", "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def track_failure(reason):
        key = reason[:100]
        APIdedup._failure_cache[key] = APIdedup._failure_cache.get(key, 0) + 1

    @task(1)  # Меньшая весомость
    def get_events(self):
        self.client.get("/events/get_events", name="Get events")

    @task(2)
    def post_events(self):
        try:
            with APIdedup._data_lock:
                data_event = random.choice(self.test_data)

            with self.client.post("/events/event_post/",
                                  name="Post events",
                                  json=data_event,
                                  headers={"Content-Type": "application/json"},
                                  catch_response=True) as response:
                if response.status_code == 0:
                    error_msg = "No response from server (status 0)"
                    self.track_failure(error_msg)
                    response.failure(error_msg)
                elif response.status_code == 200:
                    response.success()
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.track_failure(error_msg)
                    response.failure(error_msg)
        except Exception as e:
            error_msg = str(e)
            self.track_failure(error_msg)
            logging.error(f"Request failed: {error_msg}")

    def on_stop(self):
        if APIdedup._failure_cache:
            logging.info("Failure statistics:")
            for reason, count in sorted(APIdedup._failure_cache.items(), key=lambda x: -x[1]):
                logging.info(f"{count}x {reason}")
