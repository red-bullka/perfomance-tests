from clients.http.gateway.users.client import build_users_gateway_http_client
from clients.http.gateway.account.client import build_accounts_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client


def main() -> None:
    """
    Скрипт:
      1) создаёт пользователя,
      2) открывает дебетовый счёт,
      3) создаёт операцию пополнения счёта,
      4) печатает результаты.
    """
    users_client = build_users_gateway_http_client()
    accounts_client = build_accounts_gateway_http_client()
    operations_client = build_operations_gateway_http_client()

    create_user_resp = users_client.create_user()
    print("Create user response:", create_user_resp)
    user_id = create_user_resp.user.id

    open_debit_acc_resp = accounts_client.open_debit_card_account(user_id=user_id)
    print("Open debit card account response:", open_debit_acc_resp)

    account = open_debit_acc_resp.account
    account_id = account.id

    first_card_id = account.cards[0].id

    top_up_resp = operations_client.make_top_up_operation(
        card_id=first_card_id,
        account_id=account_id,
    )
    print("Make top up operation response:", top_up_resp)


if __name__ == "__main__":
    main()
