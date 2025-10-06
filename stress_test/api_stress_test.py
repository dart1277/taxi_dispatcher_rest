import random
import string
import time

from dotenv import dotenv_values
from locust import HttpUser, task, between

config = dotenv_values(".dotenv")


def random_email():
    """Generate a random email address."""
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"{name}@{domain}.com"


class OrderUser(HttpUser):
    wait_time = between(0, 0)
    host = f"{config['API_URL']}/order"

    @task
    def send_orders(self):
        n_requests = int(config["N_REQUESTS"])
        test_interval = int(config["INTERVAL"])
        base_wait = test_interval / n_requests
        jitters = [random.uniform(-0.2 * base_wait, 0.2 * base_wait) for _ in range(n_requests)]

        total_jitter = sum(jitters)
        adjustment = (test_interval - total_jitter) / n_requests
        waits = [max(0, base_wait + jitter + adjustment) for jitter in jitters]

        for i in range(int(n_requests)):
            dto = {
                "user_id": random_email(),
                "src_x": random.randint(1, 100),
                "src_y": random.randint(1, 100),
                "dst_x": random.randint(1, 100),
                "dst_y": random.randint(1, 100)
            }

            with self.client.post(OrderUser.host, json=dto, catch_response=True) as resp:
                if resp.status_code < 300:
                    resp.success()
                else:
                    resp.failure(f"Failed: {resp.status_code}")
                #time.sleep(waits[i])

        # time.sleep(int(config["WAIT_TIME"]))
