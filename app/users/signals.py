from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from users.models import User
from utils.blockchain import create_wallet


@receiver(post_save, sender=User)
def process_user(sender, instance, created, **kwargs):
    if created:
        instance.set_password(instance.password)

        wallet = create_wallet()

        instance.wallet_public_key = wallet.publicKey
        instance.wallet_private_key = wallet.privateKey
        instance.save()
