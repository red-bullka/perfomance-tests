import time

from clients.http.gateway.users.client import (
    CreateUserRequestDict,
    build_users_gateway_http_client
)

users_gateway_client = build_users_gateway_http_client()

create_user_request = CreateUserRequestDict(
    email=f"user.{time.time()}@example.com",
    lastName="string",
    firstName="string",
    middleName="string",
    phoneNumber="string"
)
create_user_response = users_gateway_client.create_user_api(create_user_request)
create_user_response_data = create_user_response.json()
print("Create user data:", create_user_response_data)


get_user_response = users_gateway_client.get_user_api(create_user_response_data['user']['id'])
get_user_response_data = get_user_response.json()
print("Get user data:", get_user_response_data)