import lib.nft_data as nft_data
import requests, json


# print(nft_data.get_nft_type(9969))
# print(nft_data.get_nft_type(2156))
# print(nft_data.get_nft_type(61))
# print(nft_data.get_nft_type(4527))
# print(nft_data.get_nft_type(9999))

# print(nft_data.get_rarity(9969))
# print(nft_data.get_collection_stats())
stats = nft_data.get_collection_stats()
print(nft_data.get_estimeated_price(2156, stats))

def get_eth_doe_price():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://api.coingecko.com/api/v3/simple/price?ids=dogsofelon&vs_currencies=eth"
    return requests.get(url, headers=headers).json()['dogsofelon']['eth']

print(get_eth_doe_price())