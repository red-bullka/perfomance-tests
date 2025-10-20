from httpx import Client, URL, QueryParams, Response
from typing import Any
class HttpClient:
    def __init__(self, client: Client):
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None ) -> Response:
        self.client.get(url, params=params)
        return self.client.get(url, params=params)

    def post(self, url: URL | str, json: Any | None = None) -> Response:
        return self.client.post(url, json=json)
