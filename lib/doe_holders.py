
def all_doe_stake_transactions():
    data = {
        'module': 'account',
        'action': 'txlist',
        'address':'0x60C6b5DC066E33801F2D9F2830595490A3086B4e',
        'startblock':'13554136',
        'endblock':'99999999',
        # 'page': '1',
        # 'offset': '5',
        'sort': 'asc',
        'apikey': hidden_details.etherscan_key,
    }
    return requests.get("https://api.etherscan.io/api", data=data).json()['result']

def dump_all_stakers():
    addresses = []
    dump = all_doe_stake_transactions()
    for tx in dump:
        addr = tx['from']
        if addr not in addresses:
            addresses.append(addr)