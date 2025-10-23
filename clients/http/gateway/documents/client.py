from httpx import Response

from clients.http.client import HttpClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.documents.schema import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema
)


class DocumentsGatewayHTTPClient(HttpClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """GET /api/v1/documents/tariff-document/{account_id} — получить тариф по счёту."""
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """GET /api/v1/documents/contract-document/{account_id} — получить контракт по счёту."""
        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """
        Выполняет запрос тарифа и возвращает Pydantic-модель ответа.
        :param account_id: Идентификатор счёта.
        """
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        """
        Выполняет запрос контракта и возвращает Pydantic-модель ответа.
        :param account_id: Идентификатор счёта.
        """
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Возвращает готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
