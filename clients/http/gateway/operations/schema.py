"""
Этот модуль содержит Pydantic-модели для работы с API операций (/api/v1/operations).
"""
from datetime import datetime
from enum import StrEnum
from tools.fakers import fake
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class OperationStatus(StrEnum):
    """Статусы, которые может принимать операция."""
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"


class OperationType(StrEnum):
    """Типы, которые может принимать операция."""
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    PURCHASE = "PURCHASE"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"
    UNSPECIFIED = "UNSPECIFIED"


class OperationSchema(BaseModel):
    """Описание сущности операции."""
    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str
    created_at: datetime = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """Описание JSON-объекта чека (receipt)."""
    url: HttpUrl
    document: str


class OperationsSummarySchema(BaseModel):
    """Сводная статистика по операциям."""
    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


class GetOperationsQuerySchema(BaseModel):
    """Query-параметры для получения списка операций."""
    model_config = ConfigDict(populate_by_name=True)
    account_id: str = Field(alias="accountId")


class MakeOperationRequestSchema(BaseModel):
    """Базовое тело POST-запроса на создание операции."""
    model_config = ConfigDict(populate_by_name=True)

    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")

    status: OperationStatus = Field(default_factory=lambda: fake.enum(OperationStatus))
    amount: float = Field(default_factory=fake.amount)


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    """Тело POST-запроса на создание операции покупки (с категорией)."""
    # Поле с автоматической генерацией данных
    category: str = Field(default_factory=fake.category)


class GetOperationResponseSchema(BaseModel):
    operation: OperationSchema


class GetOperationsResponseSchema(BaseModel):
    operations: list[OperationSchema]


class GetOperationReceiptResponseSchema(BaseModel):
    receipt: OperationReceiptSchema


class GetOperationsSummaryResponseSchema(BaseModel):
    summary: OperationsSummarySchema


class CreateOperationResponseSchema(BaseModel):
    """Ответ на любой make-* запрос."""
    operation: OperationSchema