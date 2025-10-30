from locust import User, between, task

from clients.http.gateway.users.client import (
    UsersGatewayHTTPClient,
    build_users_gateway_locust_http_client
)
from clients.http.gateway.account.client import (
    AccountsGatewayHTTPClient,
    build_accounts_gateway_locust_http_client
)
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.account.schema import OpenDebitCardAccountResponseSchema


class OpenDebitCardAccountScenarioUser(User):
    """
    Нагрузочный сценарий:
    1. Создаёт нового пользователя (через UsersGatewayHTTPClient)
    2. Открывает дебетовый счёт для этого пользователя (через AccountsGatewayHTTPClient)
    """

    host = "localhost"
    wait_time = between(1, 3)

    users_gateway_client: UsersGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient

    create_user_response: CreateUserResponseSchema
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema

    def on_start(self) -> None:
        """
        Метод вызывается один раз при запуске виртуального пользователя.
        Создаёт пользователя и открывает ему дебетовый счёт.
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)

        self.create_user_response = self.users_gateway_client.create_user()

        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            self.create_user_response.user.id
        )

    @task
    def reopen_debit_card_account(self):
        """
        Основная нагрузочная задача:
        выполняет повторное открытие дебетового счёта для разных пользователей.
        """
        self.accounts_gateway_client.open_debit_card_account(
            self.create_user_response.user.id
        )
