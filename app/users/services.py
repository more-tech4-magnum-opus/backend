from random import shuffle

from django.conf import settings

from blockchain.services import transact_from_admin
from .models import Clan, User
import requests as r
import json


def end_season():
    mx_value = -1
    mx_clan = None
    for clan in Clan.objects.all():
        if sum(map(lambda user: user.respect, clan.users.all())) > mx_value:
            mx_value = sum(map(lambda user: user.respect, clan.users.all()))
            mx_clan = clan
    for user in mx_clan.users.all():
        transact_from_admin(user, 100)
    Clan.objects.all().delete()

    for user in User.objects.filter(type=User.WorkerType.WORKER):
        if user.salary > 0:
            transact_from_admin(user, user.salary)


def create_chat(clan: Clan):
    user_list = list(map(lambda user: user.telegram, clan.users.all()))
    if len(user_list):
        r.post(
            f"{settings.TELEGRAM_API}/create-chat",
            data=json.dumps({"chat_name": clan.name, "users": user_list}),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )


def create_season():
    if len(Clan.objects.all()):
        end_season()

    users = list(User.objects.filter(type=User.WorkerType.WORKER))
    shuffle(users)
    clan = None
    for index, user in enumerate(users):
        if index % 5 == 0:
            clan = Clan.objects.create()
        user.clan = clan
        user.save()
    for clan in Clan.objects.all():
        create_chat(clan)
