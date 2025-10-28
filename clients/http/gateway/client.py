from httpx import Client
from locust.env import Environment
import logging
from clients.http.event_hooks.locust_event_hook import (
    locust_request_event_hook,
    locust_response_event_hook
)


def build_gateway_http_client() -> Client:
    return Client(timeout=100, base_url='http://localhost:8003')


def build_gateway_locust_http_client(environment: Environment) -> Client:
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return Client(
        timeout=100,
        base_url='http://localhost:8003',
        event_hooks={
            "request": [locust_request_event_hook],
            "response": [locust_response_event_hook(environment)]
        }
    )
