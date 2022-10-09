from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from conf import settings
from users.models import User
from utils.blockchain import create_wallet, send_matic


@receiver(post_save, sender=User)
def process_user(sender, instance, created, **kwargs):
    if created:
        instance.set_password(instance.password)

        wallet = create_wallet()
        send_matic(settings.MAIN_WALLET, wallet.publicKey, 0.1)

        instance.wallet_public_key = wallet.publicKey
        instance.wallet_private_key = wallet.privateKey
        instance.save()
