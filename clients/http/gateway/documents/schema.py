from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum


class DocumentSchema(BaseModel):
    """Универсальная структура документа (тариф/контракт)."""
    url: str
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """Структура ответа на запрос тарифа по счёту."""
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """Структура ответа на запрос контракта по счёту."""
    contract: DocumentSchema

