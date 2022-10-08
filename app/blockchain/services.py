from django.conf import settings

from blockchain.models import Transaction, AdminTransaction
from users.models import User
from utils.blockchain import transfer_rubbles


def list_user_transactions(user: User) -> list:
    transaction = []
    qs = (
        user.transactions_to.all()
        | user.transactions_from.all()
        | user.admin_transactions.all()
    )
    qs.order_by("created")
    username = user.username
    for el in qs:  # type: Transaction
        transaction.append(
            {
                "type": "addition" if el.user_from.username == username else "transfer",
                "user_from": el.user_from.username,
                "user_to": el.user_to.username,
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

