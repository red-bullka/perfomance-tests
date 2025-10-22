from __future__ import annotations

from httpx import Response, QueryParams

from clients.http.client import HttpClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.operations.schema import (
    GetOperationsQuerySchema,
    MakeOperationRequestSchema,
    MakePurchaseOperationRequestSchema,
    GetOperationResponseSchema,
    GetOperationsResponseSchema,
    GetOperationReceiptResponseSchema,
    GetOperationsSummaryResponseSchema,
    CreateOperationResponseSchema,
)


class OperationsGatewayHTTPClient(HttpClient):

    def get_operation_api(self, operation_id: str) -> Response:
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        params = QueryParams(**query.model_dump(by_alias=True))
        return self.get("/api/v1/operations", params=params)

    def get_operations_summary_api(self, query: GetOperationsQuerySchema) -> Response:
        params = QueryParams(**query.model_dump(by_alias=True))
        return self.get("/api/v1/operations/operations-summary", params=params)

    def make_fee_operation_api(self, request: MakeOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-fee-operation",
                         json=request.model_dump(by_alias=True))

    def make_top_up_operation_api(self, request: MakeOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-top-up-operation",
                         json=request.model_dump(by_alias=True))

    def make_cashback_operation_api(self, request: MakeOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-cashback-operation",
                         json=request.model_dump(by_alias=True))

    def make_transfer_operation_api(self, request: MakeOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-transfer-operation",
                         json=request.model_dump(by_alias=True))

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-purchase-operation",
                         json=request.model_dump(by_alias=True))

    def make_bill_payment_operation_api(self, request: MakeOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-bill-payment-operation",
                         json=request.model_dump(by_alias=True))

    def make_cash_withdrawal_operation_api(self, request: MakeOperationRequestSchema) -> Response:
        return self.post("/api/v1/operations/make-cash-withdrawal-operation",
                         json=request.model_dump(by_alias=True))

    # --- High-level ---

    def get_operation(self, operation_id: str) -> GetOperationResponseSchema:
        resp = self.get_operation_api(operation_id)
        return GetOperationResponseSchema.model_validate_json(resp.text)

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseSchema:
        resp = self.get_operation_receipt_api(operation_id)
        return GetOperationReceiptResponseSchema.model_validate_json(resp.text)

    def get_operations(self, account_id: str) -> GetOperationsResponseSchema:
        query = GetOperationsQuerySchema(account_id=account_id)
        resp = self.get_operations_api(query)
        return GetOperationsResponseSchema.model_validate_json(resp.text)

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseSchema:
        query = GetOperationsQuerySchema(account_id=account_id)
        resp = self.get_operations_summary_api(query)
        return GetOperationsSummaryResponseSchema.model_validate_json(resp.text)

    def make_fee_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakeOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_fee_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)

    def make_top_up_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakeOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_top_up_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)

    def make_cashback_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakeOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_cashback_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)

    def make_transfer_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakeOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_transfer_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)

    def make_purchase_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakePurchaseOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_purchase_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakeOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_bill_payment_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> CreateOperationResponseSchema:
        request = MakeOperationRequestSchema(card_id=card_id, account_id=account_id)
        resp = self.make_cash_withdrawal_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(resp.text)


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
