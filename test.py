from web3 import Web3
import web3
import lib.nft_data as nft_data
import requests, json
import hidden_details, datetime
import contracts.doe_doe_staking_contract as doe_doe_staking_contract


# print(nft_data.get_nft_type(9969))
# print(nft_data.get_nft_type(2156))
# print(nft_data.get_nft_type(61))
# print(nft_data.get_nft_type(4527))
# print(nft_data.get_nft_type(9999))

# print(nft_data.get_rarity(9969))
# print(nft_data.get_collection_stats())
# stats = nft_data.get_collection_stats()
# print(nft_data.get_estimeated_price(2156, stats))

def get_eth_doe_price():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://api.coingecko.com/api/v3/simple/price?ids=dogsofelon&vs_currencies=eth"
    return requests.get(url, headers=headers).json()['dogsofelon']['eth']

# print(get_eth_doe_price())

# 13290468 -- sept
def dump_addr():
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


# w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
# staking_holders = []
# with open('bin/allAddrDoeStake-20220415.txt') as f:
#     staking_holders = f.read().splitlines()

other = json.load(open('bin/other.json'))
last_hdlrs = {}
for h in other:
    last_hdlrs[Web3.toChecksumAddress(h)] = other[h]

# print(last_hdlrs)

print(dict(sorted({'0': 0, '2': 1, '1': 2, '4': 3, '3': 4}.items(), key=lambda item: item[1])))


hodlers = json.load(open('bin/hodlers-20220415.json'))
hodlers_sorted = dict(sorted(hodlers['hodlers'].items(), key=lambda item: item[1], reverse=True))
print(hodlers_sorted)
hodlers['hodlers'] = hodlers_sorted

with open('bin/hodlers_20220415_sorted.json', 'w') as f:
     json.dump(hodlers, f)

# for h in other:
#     hodlers['hodlers'][h] = other[h]

# print(hodlers)

# with open('bin/hodlers2.json', 'w') as f:
#     json.dump(hodlers, f)


# print(len(staking_holders))
# # 0x8a2B212cA369f4893F298dD0C4aebE0E75C8396e
# # 0x8a2B212cA369f4893F298dD0C4aebE0E75C8396e
# # 0x5dA93cF2d5595Dd68Daed256DFbFF62c7ebBB298

# # print(doe_doe_staking_contract.get_balances(w3_eth, Web3.toChecksumAddress(staking_holders[0])))
# # print(doe_doe_staking_contract.get_balances(w3_eth, Web3.toChecksumAddress(staking_holders[2])))

# hodlers = {
#     'date': "20220415",
#     'hodlers' : {}
#     }
# def get_and_print(w3_eth, addr):
#     check_addr = Web3.toChecksumAddress(addr)
#     bal = doe_doe_staking_contract.get_balances(w3_eth, Web3.toChecksumAddress(addr))
#     balance = float(bal['Staked'] + bal['Rewards'])
#     print(f"{addr}: {balance}")
#     hodlers['hodlers'][check_addr] = balance

# i = 0
# for holder in staking_holders:
#     get_and_print(w3_eth, holder)
#     i = i + 1
#     if (i % 50) == 0:
#         with open("bin/hodlers.json", 'w') as f:
#             json.dump(hodlers, f)
#             print(f"Dunmped: {i}")

# json.dump(hodlers, f)
# print("Dunmped: ALLLLL")

