from xml.dom import pulldom
from pydantic import BaseModel
import requests as r

URL = 'https://hackathon.lsp.team/hk'

"""TODO: Сделать обвязку апишки блокчейна"""


class WalletCreation(BaseModel):
    publicKey: str
    privateKey: str


def create_wallet() -> WalletCreation:
    response = r.post(URL+'/v1/wallets/new')
    data = response.json()
    return WalletCreation(publicKey=data['publicKey'], privateKey=data['privateKey'])
