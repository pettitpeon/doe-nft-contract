from web3 import Web3
import contracts.slp_doe_staking_contract as slp_doe_staking_contract
import contracts.slp_eth_doe_contract as slp_eth_doe_contract
import contracts.doe_doe_staking_contract as doe_doe_staking_contract
import contracts.doe_nft_staking_contract as doe_nft_staking_contract
import contracts.nft_contract as nft_contract
import contracts.doe_token_contract as doe_token_contract
import hidden_details as hidden_details
import lib.nft_data as nft_data
import requests, json


def get_arbitrum_worth(w3, wallet):
    balance = slp_doe_staking_contract.get_balances(w3, wallet)
    slp_data = slp_eth_doe_contract.get_data(w3, wallet)

    mySlpSupply = balance['Staked']  + slp_data['liquidity']
    mySupplyPer = mySlpSupply / slp_data['totalSupply']

    return {
        "SLP_ETH" : mySupplyPer * slp_data['reserves']['ETH'],
        "SLP_DOE" : mySupplyPer * slp_data['reserves']['DOE'],
        "SLP_rewards" : balance['Rewards'],
    }

def get_doe_doe(w3, wallet):
    return doe_doe_staking_contract.get_balances(w3, wallet)

def get_doe_nft(w3, wallet):
    uint128Max = 340282366920938463463374607431768211455 # 2**128 - 1
    data = doe_nft_staking_contract.get_data(w3, wallet)
    secondsLeft = 0.0
    if len(data['getTokensOf']) > 0:
        rewardPerTokenPending = data['userRewardPerTokenPaid'] - data['rewardPerToken']
        if (rewardPerTokenPending < 0):
            rewardPerTokenPending = rewardPerTokenPending + uint128Max
        
        secondsLeft = (rewardPerTokenPending / data['rewardRate']) * data['totalSupply']
    return {
        "secondsLeft": secondsLeft,
        "daysLeft": secondsLeft / (60*60*24),
        "Rewards": data['earned'],
        "totalSupply" : data['totalSupply'],
        "StakedNFTs" : data['getTokensOf'],
    }

def get_nft(w3, wallet):
    return nft_contract.get_data(w3, wallet)

def get_cummulated_price(nfts_total, eth_doe_price, stats):
    cummulated = 0.0
    for nft in nfts_total:
        type = nft_data.get_nft_type(nft)
        estimated_stats = nft_data.get_estimated_price(nft, stats)
        estimated = estimated_stats['estimated']
        rarity = estimated_stats['rarity']
        cummulated = cummulated + estimated
        print(f"Estimated #{nft}[{rarity: >4}] {type: >9}: {estimated: 7,.4f} ETH, {estimated/eth_doe_price: 10,.2f} DOE")

    return cummulated

def get_eth_doe_price():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://api.coingecko.com/api/v3/simple/price?ids=dogsofelon&vs_currencies=eth"
    return requests.get(url, headers=headers).json()['dogsofelon']['eth']

#############################################################
wallet = hidden_details.user_wallet
#############################################################

eth_doe_price = get_eth_doe_price()
w3_arb = Web3(Web3.HTTPProvider(hidden_details.arbirum_mainnet))
w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))

arbitrum = get_arbitrum_worth(w3_arb, wallet)
doe_doe = get_doe_doe(w3_eth, wallet)
doe_nft = get_doe_nft(w3_eth, wallet)
nft = get_nft(w3_eth, wallet)

doe_main_wallet = doe_token_contract.get_main_balance(w3_eth, wallet)
doe_arb_wallet = doe_token_contract.get_arb_balance(w3_arb, wallet)
arb_doe_total = arbitrum['SLP_DOE'] + arbitrum['SLP_rewards'] + doe_arb_wallet
doe_doe_total = doe_doe['Staked'] + doe_doe['Rewards']
doe_nft_total = doe_nft['Rewards']
nfts_total = [*doe_nft['StakedNFTs'], *nft['walletInventory']]

print(f"Main wallet:     {doe_main_wallet: 10.2f} DOE")
print(f"DOE:DOE Staked:  {doe_doe['Staked']: 10.2f} DOE")
print(f"DOE:DOE Rewards: {doe_doe['Rewards']: 10.2f} DOE")
print(f"DOE:DOE Total:   {doe_doe_total: 10.2f} DOE")
print(f"SLP:             {arbitrum['SLP_ETH']: 10.2f} ETH")
print(f"SLP:             {arbitrum['SLP_DOE']: 10.2f} DOE")
print(f"SLP:DOE Rewards: {arbitrum['SLP_rewards']: 10.2f} DOE")
print(f"Arbitrum wallet: {doe_arb_wallet: 10.2f} DOE")
print(f"Arbitrum Total:  {arb_doe_total: 10.2f} DOE")
print(f"DOE:NFT Rewards: {doe_nft_total: 10.2f} DOE")
print(f"Days left to claim: {doe_nft['daysLeft']: 7.2f} days")
token_total = arb_doe_total + doe_doe_total + doe_nft_total + doe_main_wallet
print("-------------------------------------------------------")
print('Token total: {:,.2f} DOE'.format(token_total))
print("")

cummulated = get_cummulated_price(nfts_total, eth_doe_price, nft_data.get_collection_stats())
cumalated_doe = cummulated / eth_doe_price
print(f"NFT staked:   {doe_nft['StakedNFTs']}: {len(doe_nft['StakedNFTs'])}")
print(f"NFT unstaked: {nft['walletInventory']}: {len(nft['walletInventory'])}")
print(f"NFTs total: {nfts_total}: {len(nfts_total)}")
print("-------------------------------------------------------")
print(f"NFTs value: {cummulated:,.3f} ETH")
print(f"NFTs value: {cumalated_doe:,.2f} DOE")
print("")
print("=======================================================")
print(f"GRAND TOTAL: {cumalated_doe + float(token_total):,.2f}")