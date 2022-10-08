from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from blockchain.models import Transaction
from utils.blockchain import get_balance, transfer_rubbles


@receiver(pre_save, sender=Transaction)
def validate_create_transaction(sender, instance: Transaction, **kwargs):
    # validate transaction
    if instance.user_from == instance.user_to:
        raise ValidationError("Cannot transfer to yourself")

    if instance.amount == 0:
        raise ValidationError("Cannot transfer 0 money")

    #  Potential Race condition, use transaction with atomics in prod
    user_from_money = int(get_balance(instance.user_from.wallet_public_key).coins)
    if instance.user_from.money != user_from_money:
        instance.user_from.money = user_from_money
        instance.user_from.save(update_fields=["money"])

    if user_from_money - instance.amount <= 0:
        raise ValidationError(
            f"{instance.user_from.username} doesn't have enough money"
        )

    transaction = transfer_rubbles(
        instance.user_from.wallet_private_key,
        instance.user_to.wallet_public_key,
        amount=instance.amount,
    )
    instance.user_from.money -= instance.amount
    instance.user_from.save(update_fields=["money"])

    instance.user_to.money += instance.amount
    instance.user_to.save(update_fields=["money"])

    instance.hash = transaction.transaction_hash
