from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

user = User(id=1, name="Alice", email="alice@example.com")
print(user)

class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address  # Вложенная модель

user = User(id=1, name="Alice", address={"city": "New York", "zip_code": "10001"})
print(user.address.city)  # "New York"
