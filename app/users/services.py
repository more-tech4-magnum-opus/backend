from random import shuffle

from django.conf import settings

from .models import Clan, User
from utils.blockchain import transfer_rubbles
import requests as r
import json


def end_season():
    mx_value = -1
    mx_clan = None
    for clan in Clan.objects.all():
        if sum(map(lambda user: user.respect, clan.user_set.all())) > mx_value:
            mx_value = sum(map(lambda user: user.respect, clan.user_set.all()))
            mx_clan = clan
    for user in mx_clan.user_set.all():
        transfer_rubbles(
            settings.MAIN_WALLET,
            user.wallet_public_key,
            100,
        )
    Clan.objects.all().delete()


def create_chat(clan: Clan):
    user_list = list(map(lambda user: user.telegram, clan.user_set.all()))
    if len(user_list):
        r.post(
            f"{settings.TELEGRAM_API}/create-chat",
            data=json.dumps({"chat_name": clan.name, "users": user_list}),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )


def create_season():
    if len(Clan.objects.all()):
        end_season()

    users = list(User.objects.all())
    shuffle(users)
    clan = None
    for index, user in enumerate(users):
        if (index % 10 == 0) or (index == len(users) - 1):
            if clan is not None:
                create_chat(clan)
            clan = Clan.objects.create()
        user.clan = clan
        user.save()
    if len(users) % 10 != 0:
        create_chat(clan)
