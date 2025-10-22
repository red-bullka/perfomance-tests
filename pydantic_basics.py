"""
{
  "account": {
    "id": "string",
    "type": "UNSPECIFIED",
    "cards": [
      {
        "id": "string",
        "pin": "string",
        "cvv": "string",
        "type": "UNSPECIFIED",
        "status": "UNSPECIFIED",
        "accountId": "string",
        "cardNumber": "string",
        "cardHolder": "string",
        "expiryDate": "2025-10-21",
        "paymentSystem": "UNSPECIFIED"
      }
    ],
    "status": "UNSPECIFIED",
    "balance": 0
  }
}
"""
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
import uuid
from datetime import date


class CardSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    id: str
    pin: str
    cvv: str
    type: str
    status: str
    account_id: str = Field(alias="accountId")
    card_number: str = Field(alias="cardNumber")
    card_holder: str = Field(alias="cardHolder")
    expiry_date: date = Field(alias="expiryDate")
    payment_system: str = Field(alias="paymentSystem")


class AccountSchema(BaseModel):
    id: str = Field(alias="id")
    type: str
    cards: list[CardSchema]
    status: str
    balance: float


account_default_model = AccountSchema(
    id="account-id",
    type="CREDIT-CART",
    cards=[
        CardSchema(
            id="card-id",
            pin="2222",
            cvv="532",
            type="PHYSICAL",
            status="ACTIVE",
            accountId="ACCOUNT-ID",
            cardNumber="1234-1234-1234",
            cardHolder="Masha Kasha",
            expiryDate=date(2027,2,25),
            paymentSystem="VISA"
        )
    ],
    status="ACTIVE",
    balance=100.57
)
print('Account default model: ', account_default_model)

account_dict = {
    "id": "account-id",
    "type": "CREDIT-CART",
    "cards": [
        {
            "id": "card-id",
            "pin": "2222",
            "cvv": "532",
            "type": "PHYSICAL",
            "status": "ACTIVE",
            "accountId": "ACCOUNT-ID",
            "cardNumber": "1234-1234-1234",
            "cardHolder": "Masha Kasha",
            "expiryDate": date(2027,2,25),
            "paymentSystem": "VISA"
        }

    ],
    "status": "ACTIVE",
    "balance": 777.11
}
account_dict_model = AccountSchema(**account_dict)
print('Account dict model: ', account_dict_model)
print(account_dict_model.model_dump())

account_json = """
{
    "id": "account-id",
    "type": "CREDIT_CARD",
    "cards": [
        {
            "id": "card-id",
            "pin": "1234",
            "cvv": "123",
            "type": "PHYSICAL",
            "status": "ACTIVE",
            "accountId": "account-id",
            "cardNumber": "1234123412341234",
            "cardHolder": "Alise Smith",
            "expiryDate": "2027-03-25",
            "paymentSystem": "VISA"
        }
    ],
    "status": "ACTIVE",
    "balance": 777.11
}
"""

account_json_model = AccountSchema.model_validate_json(account_json)
print("Account JSON model:", account_json_model)