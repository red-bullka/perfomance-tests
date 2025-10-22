from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum


class CardType(StrEnum):
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(StrEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class CardPaymentSystem(StrEnum):
    MASTERCARD = "MASTERCARD"
    VISA = "VISA"


class CardSchema(BaseModel):
    """
    Описание структуры карты.
    """
    id: str
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: str = Field(alias='accountId')
    card_number: str = Field(alias='cardNumber')
    card_holder: str = Field(alias='cardHolder')
    expiry_date: str = Field(alias='expiryDate')
    payment_system: CardPaymentSystem = Field(alias='paymentSystem')


class IssueVirtualCardRequestSchema(BaseModel):
    """
    Структура данных для выпуска виртуальной карты.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')


# Добавили описание структуры ответа выпуска виртуальной карты
class IssueVirtualCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска виртуальной карты.
    """
    card: CardSchema


class IssuePhysicalCardRequestSchema(BaseModel):
    """
    Структура данных для выпуска физической карты.
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias='userId')
    account_id: str = Field(alias='accountId')


# Добавили описание структуры ответа выпуска физической карты
class IssuePhysicalCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска физической карты.
    """
    card: CardSchema
