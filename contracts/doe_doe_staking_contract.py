from web3 import Web3
import contracts.doe_doe_abi as doe_doe_abi
import requests, datetime

contract_address = "0x60C6b5DC066E33801F2D9F2830595490A3086B4e"

def get_balances(w3, wallet):
    contract = w3.eth.contract(address=contract_address, abi=doe_doe_abi.get_abi())
    balanceOf =  Web3.fromWei(contract.functions.balanceOf(wallet).call(), "ether")
    earned = Web3.fromWei(contract.functions.earned(wallet).call(), "ether")

    return {
        "Staked": balanceOf,
        "Rewards": earned,
        }


def all_doe_stake_transactions(api_key):
    data = {
        'module': 'account',
        'action': 'txlist',
        'address': contract_address,
        'startblock':'13554136',
        'endblock':'99999999',
        'sort': 'asc',
        'apikey': api_key,
    }
    return requests.get("https://api.etherscan.io/api", data=data).json()['result']

def dump_all_stakers():
    addresses = []
    dump = all_doe_stake_transactions()
    for tx in dump:
        addr = tx['from']
        if addr not in addresses:
            addresses.append(addr)

