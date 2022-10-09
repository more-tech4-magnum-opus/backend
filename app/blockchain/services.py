from itertools import chain

from django.conf import settings
from rest_framework.exceptions import ValidationError

from blockchain.models import Transaction, AdminTransaction
from users.models import User
from utils.blockchain import transfer_rubbles, get_balance


def list_user_transactions(user: User) -> list:
    transaction = []
    l = (
        [x for x in user.transactions_to.all()]
        + [x for x in user.transactions_from.all()]
        + [x for x in user.admin_transactions.all()]
    )
    l.sort(
        key=lambda instance: instance.created, reverse=True
    )
    username = user.username
    for el in l:  # type: Transaction
        if not (t := el.t_type):
            t = "to" if el.user_from.username == username else "from"

        transaction.append(
            {
                "type": t,
                "user_from": el.user_from_username,
                "user_to": el.user_to_username,
                "amount": el.amount,
            }
        )

    return transaction


def transact_from_admin(user: User, amount: int):
    priv_key = settings.MAIN_WALLET
    t = transfer_rubbles(priv_key, user.wallet_public_key, amount)
    AdminTransaction.objects.create(
        type="SALARY", amount=amount, user=user, hash=t.transaction_hash
    )
    user.money += amount
    user.save(update_fields=["money"])


def transact_to_admin(user: User, amount: int):
    user_from_money = int(get_balance(user.wallet_public_key).coins)
    if user.money != user_from_money:
        user.money = user_from_money
        user.save(update_fields=["money"])

    if user_from_money - amount < 0:
        raise ValidationError("Not enough money")

    t = transfer_rubbles(user.wallet_private_key, settings.PUB_KEY, amount)
    print(t.transaction_hash)
    user.money -= amount
    user.save(update_fields=["money"])

    AdminTransaction.objects.create(
        type="PAYMENT", amount=amount, user=user, hash=t.transaction_hash
    )
