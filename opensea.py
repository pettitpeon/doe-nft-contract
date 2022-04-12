from web3 import Web3
import requests, json, decimal

def get_last_sale_price(data):
    last_sale = {}
    last_sale['token'] = data['last_sale']['payment_token']['symbol']
    last_sale['price'] = float(Web3.fromWei(int(data['last_sale']['total_price']), 'ether'))
    payment_tokens = data['collection']['payment_tokens']
    for token in payment_tokens:
        if token['symbol'] == last_sale['token']:
            last_sale['USD_now'] = token['usd_price'] * last_sale['price']
            last_sale['ETH_now'] = token['eth_price'] * last_sale['price']
    
    last_sale['USD_then'] = float(data['last_sale']['payment_token']['usd_price']) * last_sale['price']
    return last_sale

def get_nft_sale_data(id):
    contract = "0xd8cdb4b17a741dc7c6a57a650974cd2eba544ff7"
    url = "https://api.opensea.io/api/v1/asset"
    headers = {'User-Agent': 'Mozilla/5.0'}
    return requests.get(f"{url}/{contract}/{id}/", headers=headers).json()

data = get_nft_sale_data(473)
last_sale_price_eth_usd = get_last_sale_price(data)
print(last_sale_price_eth_usd)

