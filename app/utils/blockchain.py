from pydantic import BaseModel
import requests as r
import json
from time import sleep
from typing import List

URL = 'https://hackathon.lsp.team/hk'

base_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


class Wallet(BaseModel):
    publicKey: str
    privateKey: str


class WalletBalance(BaseModel):
    matic: float
    coins: float


class TransHash(BaseModel):
    transaction_hash: str


class NftInfo(BaseModel):
    uri: str
    tokens: List[int]


class TransactionHistory(BaseModel):
    hash: str
    timestamp: int
    token_name: str
    from_wallet: str
    to_wallet: str


def create_wallet() -> Wallet:
    response = r.post(URL+'/v1/wallets/new')
    data = response.json()
    return Wallet(publicKey=data['publicKey'], privateKey=data['privateKey'])


def check_transaction(trans_hash: str) -> str:
    res = r.get(URL + '/v1/transfers/status/'+trans_hash, data=json.dumps({
        'transactionHash': trans_hash
        }),
        headers=base_headers
    )
    return res.json()['status']


def transfer_rubbles(my_wallet_private_key, transfer_publick_key: str, amount: float) -> TransHash:
    response = r.post(URL+'/v1/transfers/ruble', data=json.dumps({
            "fromPrivateKey": my_wallet_private_key,
            "toPublicKey": transfer_publick_key,
            "amount": amount
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    return TransHash(transaction_hash=response.json()['transaction'])


def create_nft(wallet_public_key: str, string_url: str) -> TransHash:
    response = r.post(URL + '/v1/nft/generate', data=json.dumps(
            {
                "toPublicKey": wallet_public_key,
                "uri": string_url,
                "nftCount": 1
            }
        ),
        headers=base_headers
    )
    return TransHash(transaction_hash=response.json()['transaction_hash'])


def get_nfts(wallet_public_key: str) -> List[NftInfo]:
    res = r.get(URL+f'/v1/wallets/{wallet_public_key}/nft/balance')
    print(res.json())
    return list(
        map(
            lambda res: NftInfo(
                uri=res['uri'], 
                tokens=res['tokens']
                ),
                res.json()['balance']
            ),
        )

def get_history(wallet_public_key: str) -> List[TransactionHistory]:
    res = r.post(URL+f'/v1/wallets/{wallet_public_key}/history', data=json.dumps({
        "page": 0,
        "offset": 100,
        "sort": "asc"

    }), headers=base_headers)
    return list(
        map(
            lambda res: TransactionHistory(
                hash=res['hash'],
                timestamp=res['timeStamp'],
                token_name=res['tokenName'],
                from_wallet=res['from'],
                to_wallet=res['to']
                ),
                res.json()['history']
            ),
        )


def transfer_nft(my_private_wallet_key: str, transfer_publick_key: str, token_id: int) -> TransHash:
    res = r.post(URL+'/v1/transfers/nft', data=json.dumps(
        {
              "fromPrivateKey": my_private_wallet_key,
              "toPublicKey": transfer_publick_key,
              "tokenId": token_id
        }
    ), headers=base_headers)
    return TransHash(transaction_hash=res.json()['transaction_hash'])

def  get_balance(my_public_wallet_key: str) -> WalletBalance:
    res = r.get(URL+f'/v1/wallets/{my_public_wallet_key}/balance')
    return WalletBalance(matic=res.json()['maticAmount'], coins=res.json()['coinsAmount'])

print(get_balance('0x1a63208e5b82588320a8C24b2c595Ba5d5cbfF3f'))
