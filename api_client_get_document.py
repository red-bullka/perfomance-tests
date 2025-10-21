from typing import TypedDict
from httpx import Response
from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class DocumentDict(TypedDict):
    """Универсальная структура документа (тариф/контракт)."""
    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """Структура ответа на запрос тарифа по счёту."""
    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """Структура ответа на запрос контракта по счёту."""
    contract: DocumentDict


class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    Содержит низкоуровневые *_api и высокоуровневые методы, возвращающие уже распарсенный JSON.
    """

    # ---------- НИЗКОУРОВНЕВЫЕ МЕТОДЫ (возвращают httpx.Response) ----------

    def get_tariff_document_api(self, account_id: str) -> Response:
        """GET /api/v1/documents/tariff-document/{account_id} — получить тариф по счёту."""
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """GET /api/v1/documents/contract-document/{account_id} — получить контракт по счёту."""
        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    # ---------- ВЫСОКУРОВНЕВЫЕ МЕТОДЫ (возвращают TypedDict) ----------

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """
        Выполняет запрос тарифа и возвращает распарсенный JSON-ответ.
        :param account_id: Идентификатор счёта.
        :return: Словарь вида {'tariff': {'url': ..., 'document': ...}}
        """
        response = self.get_tariff_document_api(account_id)
        return response.json()

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """
        Выполняет запрос контракта и возвращает распарсенный JSON-ответ.
        :param account_id: Идентификатор счёта.
        :return: Словарь вида {'contract': {'url': ..., 'document': ...}}
        """
        response = self.get_contract_document_api(account_id)
        return response.json()


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Возвращает готовый к использованию DocumentsGatewayHTTPClient, сконфигурированный билдером gateway.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
