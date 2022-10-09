from time import sleep

from celery import shared_task

from conf import settings
from marketplace.models import Product
from utils.blockchain import check_transaction, get_nfts, create_nft


@shared_task
def await_nft(pk: int):
    product = Product.objects.get(pk=pk)
    url = product.image.url
    t = create_nft(settings.PUB_KEY, url)

    status = ""
    try:
        status = check_transaction(t.transaction_hash)
    except KeyError as e:
        pass

    while status != "Success":
        sleep(3)
        try:
            status = check_transaction(t.transaction_hash)
        except KeyError as e:
            pass

        print(status)
    nfts = get_nfts(settings.PUB_KEY)
    for nft in nfts:
        if nft.uri == product.image.url:
            product.token = nft.tokens[0]
            product.save(update_fields=["token"])
            return pk
