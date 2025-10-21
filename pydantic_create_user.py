from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    """
    Модель данных пользователя.

    Эта модель описывает структуру данных пользователя в системе.
    Использует alias для преобразования camelCase полей из API
    в snake_case, принятый в Python.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")

class CreateUserRequestSchema(BaseModel):
    """
    Модель запроса на создание пользователя.

    Эта модель определяет поля, необходимые для создания нового
    пользователя. Включает в себя валидацию email и использует
    alias для удобной работы с API.
    """
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")

class CreateUserResponseSchema(BaseModel):
    """
    Модель ответа с данными созданного пользователя.

    Эта модель описывает структуру ответа сервера после успешного
    создания пользователя. Содержит вложенную модель UserSchema.
    """
    user: UserSchema

if __name__ == "__main__":
    user_request_data = {
        "email": "masha.kasha@example.com",
        "lastName": "Kasha",
        "firstName": "Masha",
        "middleName": "string",
        "phoneNumber": "88005553535"
    }

    create_user_request = CreateUserRequestSchema(**user_request_data)
    print("Request Model:")
    print(create_user_request.model_dump_json(indent=2, by_alias=True))
    print("-" * 20)

    created_user_data = {
        "id": "user-12345",
        "email": "masha.kasha@example.com",
        "lastName": "Kasha",
        "firstName": "Masha",
        "middleName": "string",
        "phoneNumber": "88005553535"
    }

    create_user_response = CreateUserResponseSchema(user=created_user_data)
    print("Response Model:")
    print(create_user_response.model_dump_json(indent=2, by_alias=True))
    print("-" * 20)

    print("Доступ к данным в коде (snake_case):")
    print(f"User ID: {create_user_response.user.id}")
    print(f"User Email: {create_user_response.user.email}")
    print(f"User Last Name: {create_user_response.user.last_name}")