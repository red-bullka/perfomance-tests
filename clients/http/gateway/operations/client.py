from typing import TypedDict
from httpx import Response, QueryParams

from clients.http.client import HttpClient
from clients.http.gateway.client import build_gateway_http_client


# ---------- TypedDict: запросы ----------

class GetOperationsQueryDict(TypedDict):
    """Query-параметры для получения списка операций по счёту."""
    accountId: str


class MakeOperationRequestDict(TypedDict):
    """Базовое тело POST-запроса на создание операции."""
    status: str              # OperationStatus: FAILED | COMPLETED | IN_PROGRESS | UNSPECIFIED
    amount: float
    cardId: str              # uuid4
    accountId: str           # uuid4


class MakePurchaseOperationRequestDict(MakeOperationRequestDict):
    """Тело POST-запроса на создание операции покупки (с категорией)."""
    category: str


# ---------- TypedDict: ответы ----------

class OperationDict(TypedDict):
    """Описание сущности операции из ответов API."""
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """Описание JSON-объекта чека (receipt)."""
    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    """Сводная статистика по операциям."""
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationResponseDict(TypedDict):
    operation: OperationDict


class GetOperationsResponseDict(TypedDict):
    operations: list[OperationDict]


class GetOperationReceiptResponseDict(TypedDict):
    receipt: OperationReceiptDict


class GetOperationsSummaryResponseDict(TypedDict):
    summary: OperationsSummaryDict


class CreateOperationResponseDict(TypedDict):
    """Ответ на любой make-* запрос."""
    operation: OperationDict


# ---------- Клиент ----------

class OperationsGatewayHTTPClient(HttpClient):
    """
    Клиент для работы с эндпоинтами /api/v1/operations сервиса http-gateway.
    Содержит низкоуровневые *_api и высокоуровневые методы, возвращающие распарсенный JSON.
    """

    # === НИЗКОУРОВНЕВЫЕ МЕТОДЫ (httpx.Response) ===

    def get_operation_api(self, operation_id: str) -> Response:
        """GET /api/v1/operations/{operation_id} — получить одну операцию."""
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """GET /api/v1/operations/operation-receipt/{operation_id} — получить чек по операции."""
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """GET /api/v1/operations?accountId=... — получить список операций по счёту."""
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations_summary_api(self, query: GetOperationsQueryDict) -> Response:
        """GET /api/v1/operations/operations-summary?accountId=... — получить сводную статистику."""
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-fee-operation — создать операцию комиссии."""
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-top-up-operation — создать операцию пополнения."""
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-cashback-operation — создать операцию кэшбэка."""
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-transfer-operation — создать операцию перевода."""
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-purchase-operation — создать операцию покупки."""
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-bill-payment-operation — создать операцию оплаты счёта."""
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeOperationRequestDict) -> Response:
        """POST /api/v1/operations/make-cash-withdrawal-operation — создать операцию снятия наличных."""
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)

    # === ВЫСОКОУРОВНЕВЫЕ МЕТОДЫ (возвращают TypedDict) ===

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """Вернуть одну операцию (распарсенный JSON)."""
        resp = self.get_operation_api(operation_id)
        return resp.json()

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """Вернуть чек по операции (распарсенный JSON)."""
        resp = self.get_operation_receipt_api(operation_id)
        return resp.json()

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """Вернуть список операций по счёту (распарсенный JSON)."""
        resp = self.get_operations_api(GetOperationsQueryDict(accountId=account_id))
        return resp.json()

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """Вернуть сводную статистику по операциям счёта (распарсенный JSON)."""
        resp = self.get_operations_summary_api(GetOperationsQueryDict(accountId=account_id))
        return resp.json()

    # --- Создание операций (для простоты фиксируем статус/amount как в примерах урока) ---

    def make_fee_operation(self, card_id: str, account_id: str) -> CreateOperationResponseDict:
        request = MakeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id,
        )
        resp = self.make_fee_operation_api(request)
        return resp.json()

    def make_top_up_operation(self, card_id: str, account_id: str) -> CreateOperationResponseDict:
        request = MakeOperationRequestDict(
            status="COMPLETED",
            amount=1500.11,
            cardId=card_id,
            accountId=account_id,
        )
        resp = self.make_top_up_operation_api(request)
        return resp.json()

    def make_cashback_operation(self, card_id: str, account_id: str) -> CreateOperationResponseDict:
        request = MakeOperationRequestDict(
            status="COMPLETED",
            amount=25.50,
            cardId=card_id,
            accountId=account_id,
        )
        resp = self.make_cashback_operation_api(request)
        return resp.json()

    def make_transfer_operation(self, card_id: str, account_id: str) -> CreateOperationResponseDict:
        request = MakeOperationRequestDict(
            status="COMPLETED",
            amount=100.00,
            cardId=card_id,
            accountId=account_id,
        )
        resp = self.make_transfer_operation_api(request)
        return resp.json()

    def make_purchase_operation(self, card_id: str, account_id: str, category: str = "taxi") -> CreateOperationResponseDict:
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=77.99,
            cardId=card_id,
            accountId=account_id,
            category=category,
        )
        resp = self.make_purchase_operation_api(request)
        return resp.json()

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> CreateOperationResponseDict:
        request = MakeOperationRequestDict(
            status="COMPLETED",
            amount=999.00,
            cardId=card_id,
            accountId=account_id,
        )
        resp = self.make_bill_payment_operation_api(request)
        return resp.json()

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> CreateOperationResponseDict:
        request = MakeOperationRequestDict(
            status="COMPLETED",
            amount=300.00,
            cardId=card_id,
            accountId=account_id,
        )
        resp = self.make_cash_withdrawal_operation_api(request)
        return resp.json()


# ---------- Builder для клиента операций ----------

def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Вернуть готовый OperationsGatewayHTTPClient, сконфигурированный билдером gateway.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
