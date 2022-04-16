from web3 import Web3
import requests, json

headers = {'User-Agent': 'Mozilla/5.0'}


def get_last_sale_price(id):
    contract = "0xd8cdb4b17a741dc7c6a57a650974cd2eba544ff7"
    url = "https://api.opensea.io/api/v1/asset"
    data = requests.get(f"{url}/{contract}/{id}/", headers=headers).json()

    last_sale = {}
    try:
        last_sale['token'] = data['last_sale']['payment_token']['symbol']
        last_sale['price'] = float(Web3.fromWei(int(data['last_sale']['total_price']), 'ether'))
        payment_tokens = data['collection']['payment_tokens']
        for token in payment_tokens:
            if token['symbol'] == last_sale['token']:
                last_sale['USD_now'] = token['usd_price'] * last_sale['price']
                last_sale['ETH_now'] = token['eth_price'] * last_sale['price']
        
        last_sale['USD_then'] = float(data['last_sale']['payment_token']['usd_price']) * last_sale['price']
    except:
        last_sale['token'] = ""
        last_sale['price'] = 0.0
        last_sale['USD_now'] = 0.0
        last_sale['ETH_now'] = 0.0
        last_sale['USD_then'] = 0.0

    return last_sale

def get_rarity(id):
    data = json.load(open("bin/doeRarity.json"))
    for nft in data:
        if nft['nft_id'] == id:
            return nft['total_score']['rank']
    return -1

def get_nft_types_from_metadata():
    data = json.load(open("bin/doeRarity.json"))
    elons = []
    aliens = []
    zombies = []
    traitless = []
    for nft in data:
        if len(nft['traits_scores']) >= 9:
            if nft['traits_scores'][9]['value'] != "None":
                elons.append(nft['nft_id'])
            elif nft['traits_scores'][1]['value'] == "Alien Doge":
                aliens.append(nft['nft_id'])
            elif nft['traits_scores'][1]['value'] == "Zombie Doge":
                zombies.append(nft['nft_id'])
            elif nft['traits_scores'][10]['value'] == "3":
                traitless.append(nft['nft_id'])

    return {
        'elons': elons,
        'aliens': aliens,
        'zombies': zombies,
        'traitless': traitless,
    }

def get_nft_types():
    return json.load(open("bin/doeTypes.json"))

def get_nft_type(id):
    types = get_nft_types()
    if id > 9997:
        return 'none'
    if id in types['elons']:
        return 'elon'
    if id in types['aliens']:
        return 'alien'
    if id in types['zombies']:
        return 'zombie'
    if id in types['traitless']:
        return 'traitless'

    return 'doge'

def get_collection_stats():
    url = "https://api.opensea.io/api/v1/collection/dogs-of-elon/stats"
    data = requests.get(url, headers=headers).json()
    return {
        'thirty_day_average_price' : data['stats']['thirty_day_average_price'],
        'floor_price' : data['stats']['floor_price'],
    }

def get_rarity_bonus(rank):
    if rank < 1000:
        return 3
    if rank < 3000:
        return 1.5
    if rank < 5000:
        return 1.25
    return 1.0

def get_type_floor(floor, type):
    if type == 'zombie':
        return 1
    if type == 'alien':
        return 1.25
    if type == 'traitless':
        return 10
    if type == 'elon':
        return 15
    return floor

def get_estimated_price(id, stats):
    type = get_nft_type(id)
    averaged_floor = (stats['thirty_day_average_price'] + stats['floor_price']) / 2
    last_sale = get_last_sale_price(id)['ETH_now']
    rarity_bonus = get_rarity_bonus(get_rarity(id))
    type_floor = get_type_floor(averaged_floor, type)

    return {
        'averaged_floor': averaged_floor,
        'last_sale': last_sale,
        'rarity_bonus': rarity_bonus,
        'estimated': max(type_floor, averaged_floor * rarity_bonus, last_sale),
        'type': type
    }