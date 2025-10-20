from typing import TypedDict
from httpx import Response
from clients.http.client import HttpClient


class IssueVirtualCardRequestDict(TypedDict):
    """Структура данных для запроса выпуска виртуальной карты.

    Поля:
        userId: UUID пользователя.
        accountId: UUID счёта, к которому будет привязана карта.
    """
    userId: str
    accountId: str


class IssuePhysicalCardRequestDict(TypedDict):
    """Структура данных для запроса выпуска физической карты.

    Поля:
        userId: UUID пользователя.
        accountId: UUID счёта, к которому будет привязана карта.
    """
    userId: str
    accountId: str


class CardsGatewayHTTPClient(HttpClient):
    """Клиент для взаимодействия с эндпоинтами /api/v1/cards сервиса http-gateway.

    Реализует методы:
        - issue_virtual_card_api: Выпуск виртуальной карты.
        - issue_physical_card_api: Выпуск физической карты.
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestDict) -> Response:
        """Выпустить виртуальную карту.

        Args:
            request: Словарь (TypedDict) с полями userId и accountId.

        Returns:
            httpx.Response: Ответ сервера с информацией о созданной карте.
        """
        return self.post("/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        """Выпустить физическую карту.

        Args:
            request: Словарь (TypedDict) с полями userId и accountId.

        Returns:
            httpx.Response: Ответ сервера с информацией о созданной карте.
        """
        return self.post("/api/v1/cards/issue-physical-card", json=request)
