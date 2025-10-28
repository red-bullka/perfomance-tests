from locust.env import Environment
from httpx import Response

from clients.http.client import HttpClient, HttpClientExtensions
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client
)

from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)


class UsersGatewayHTTPClient(HttpClient):
    def get_user_api(self, user_id: str) -> Response:
        return self.get(
            f"/api/v1/users/{user_id}",
            extensions=HttpClientExtensions(route='/api/v1/users/{user_id}')
        )

    def create_user_api(self, request) -> Response:
        return self.post(f"/api/v1/users", json=request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    def create_user(self) -> CreateUserResponseSchema:
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    return UsersGatewayHTTPClient(client=build_gateway_http_client())


def build_users_gateway_locust_http_client(environment: Environment) -> UsersGatewayHTTPClient:
    return UsersGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
