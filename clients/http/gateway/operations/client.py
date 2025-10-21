from typing import TypedDict
from httpx import Response, QueryParams
from clients.http.client import HttpClient
from clients.http.gateway.client import build_gateway_http_client


class GetOperationsQueryDict(TypedDict):
    """Query-параметры для получения списка операций по счёту."""
    accountId: str


class OperationsSummaryQueryDict(TypedDict):
    """Query-параметры для получения сводной статистики операций по счёту."""
    accountId: str


class MakeOperationRequestDict(TypedDict):
    """Базовая структура тела операции (общие поля)."""
    status: str        # OperationStatus: FAILED | COMPLETED | IN_PROGRESS | UNSPECIFIED
    amount: float
    cardId: str        # uuid4
    accountId: str     # uuid4


class MakePurchaseOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции покупки (доп. поле category)."""
    category: str


class MakeFeeOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции комиссии."""


class MakeTopUpOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции пополнения."""


class MakeCashbackOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции кэшбэка."""


class MakeTransferOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции перевода."""


class MakeBillPaymentOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции оплаты по счёту."""


class MakeCashWithdrawalOperationRequestDict(MakeOperationRequestDict):
    """Тело запроса для операции снятия наличных."""


class OperationsGatewayHTTPClient(HttpClient):
    """Клиент для работы с эндпоинтами /api/v1/operations сервиса http-gateway."""

    def get_operation_api(self, operation_id: str) -> Response:
        """Получить данные конкретной операции по её идентификатору."""
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """Получить чек (receipt) по операции."""
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """Получить список операций для указанного счёта (query: accountId)."""
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations_summary_api(self, query: OperationsSummaryQueryDict) -> Response:
        """Получить сводную статистику операций для указанного счёта (query: accountId)."""
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """Создать операцию комиссии."""
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """Создать операцию пополнения."""
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """Создать операцию кэшбэка."""
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """Создать операцию перевода."""
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """Создать операцию покупки (с категорией)."""
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """Создать операцию оплаты по счёту."""
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """Создать операцию снятия наличных."""
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)


def build_documents_gateway_http_client() -> OperationsGatewayHTTPClient:
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())