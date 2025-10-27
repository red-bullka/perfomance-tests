from grpc import Channel

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import build_gateway_grpc_client
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from tools.fakers import fake


class UsersGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с UsersGatewayService.
    Предоставляет высокоуровневые методы для работы с пользователями.
    """

    def __init__(self, channel: Channel):
        """
        Инициализация клиента с указанным gRPC-каналом.

        :param channel: gRPC-канал для подключения к UsersGatewayService.
        """
        super().__init__(channel)
        self.stub = UsersGatewayServiceStub(channel)

    def get_user_api(self, request: GetUserRequest) -> GetUserResponse:
        """
        Низкоуровневый вызов метода GetUser через gRPC.

        :param request: gRPC-запрос с ID пользователя.
        :return: Ответ от сервиса с данными пользователя.
        """
        return self.stub.GetUser(request)

    def create_user_api(self, request: CreateUserRequest) -> CreateUserResponse:
        """
        Низкоуровневый вызов метода CreateUser через gRPC.

        :param request: gRPC-запрос с данными пользователя.
        :return: Ответ от сервиса с данными созданного пользователя.
        """
        return self.stub.CreateUser(request)

    def get_user(self, user_id: str) -> GetUserResponse:
        """
        Высокоуровневый метод для получения данных пользователя.

        :param user_id: UUID пользователя.
        :return: Ответ с данными пользователя.
        """
        request = GetUserRequest(id=user_id)
        return self.get_user_api(request)

    def create_user(self) -> CreateUserResponse:
        """
        Высокоуровневый метод для создания пользователя.

        :return: Ответ с данными созданного пользователя.
        """
        request = CreateUserRequest(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            middle_name=fake.middle_name(),
            phone_number=fake.phone_number()
        )
        return self.create_user_api(request)


def build_users_gateway_grpc_client() -> UsersGatewayGRPCClient:
    """
    Фабрика для создания экземпляра UsersGatewayGRPCClient.

    :return: Инициализированный клиент для UsersGatewayService.
    """
    return UsersGatewayGRPCClient(channel=build_gateway_grpc_client())
