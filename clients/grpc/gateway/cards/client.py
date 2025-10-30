from grpc import Channel
from locust.env import Environment

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import (
    build_gateway_grpc_client,
    build_gateway_locust_grpc_client
)
from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import CardsGatewayServiceStub
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse
)
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import (
    IssueVirtualCardRequest,
    IssueVirtualCardResponse
)



class CardsGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с CardsGatewayService внутри grpc-gateway.

    Содержит низкоуровневые методы (прямой вызов stub):
      - issue_virtual_card_api
      - issue_physical_card_api

    А также высокоуровневые обёртки:
      - issue_virtual_card
      - issue_physical_card
    """

    def __init__(self, channel: Channel) -> None:
        """
        Инициализация клиента.

        :param channel: общий gRPC-канал до grpc-gateway.
        """
        super().__init__(channel)
        self.stub: CardsGatewayServiceStub = CardsGatewayServiceStub(channel)

    # ---------- Низкоуровневые API-методы (прямой вызов stub) ----------

    def issue_virtual_card_api(
        self,
        request: IssueVirtualCardRequest,
    ) -> IssueVirtualCardResponse:
        """
        Прямой вызов CardsGatewayService.IssueVirtualCard.

        :param request: gRPC-запрос IssueVirtualCardRequest.
        :return: gRPC-ответ IssueVirtualCardResponse.
        """
        return self.stub.IssueVirtualCard(request)

    def issue_physical_card_api(
        self,
        request: IssuePhysicalCardRequest,
    ) -> IssuePhysicalCardResponse:
        """
        Прямой вызов CardsGatewayService.IssuePhysicalCard.

        :param request: gRPC-запрос IssuePhysicalCardRequest.
        :return: gRPC-ответ IssuePhysicalCardResponse.
        """
        return self.stub.IssuePhysicalCard(request)

    # ---------- Высокоуровневые обёртки ----------

    def issue_virtual_card(
        self,
        user_id: str,
        account_id: str,
    ) -> IssueVirtualCardResponse:
        """
        Выпуск виртуальной карты.

        :param user_id: идентификатор пользователя.
        :param account_id: идентификатор счёта.
        :return: gRPC-ответ IssueVirtualCardResponse.
        """
        request = IssueVirtualCardRequest(user_id=user_id, account_id=account_id)
        return self.issue_virtual_card_api(request)

    def issue_physical_card(
        self,
        user_id: str,
        account_id: str,
    ) -> IssuePhysicalCardResponse:
        """
        Выпуск физической карты.

        :param user_id: идентификатор пользователя.
        :param account_id: идентификатор счёта.
        :return: gRPC-ответ IssuePhysicalCardResponse.
        """
        request = IssuePhysicalCardRequest(user_id=user_id, account_id=account_id)
        return self.issue_physical_card_api(request)


def build_cards_gateway_grpc_client() -> CardsGatewayGRPCClient:
    """
    Фабрика для создания экземпляра CardsGatewayGRPCClient.

    :return: Инициализированный клиент для CardsGatewayService.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_grpc_client())


# Новый билдер для нагрузочного тестирования
def build_cards_gateway_locust_grpc_client(environment: Environment) -> CardsGatewayGRPCClient:
    """
    Функция создаёт экземпляр CardsGatewayGRPCClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр CardsGatewayGRPCClient с хуками сбора метрик.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_locust_grpc_client(environment))
