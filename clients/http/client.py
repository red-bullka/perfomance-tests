from httpx import Client, URL, QueryParams, Response

from typing import Any, TypedDict


class HttpClientExtensions(TypedDict, total=False):
    route: str


class HttpClient:
    def __init__(self, client: Client):
        self.client = client

    def get(self,
            url: URL | str,
            params: QueryParams | None = None,
            extensions: HttpClientExtensions | None = None
            ) -> Response:
        self.client.get(url, params=params)
        return self.client.get(url, params=params, extensions=extensions)

    def post(self,
             url: URL | str,
             json: Any | None = None,
             extensions: HttpClientExtensions | None = None
             ) -> Response:
        return self.client.post(url, json=json, extensions=extensions)
