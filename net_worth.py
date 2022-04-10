from web3 import Web3
import contracts.slp_doe_staking_contract as slp_doe_staking_contract
import contracts.slp_eth_doe_contract as slp_eth_doe_contract
import contracts.doe_doe_staking_contract as doe_doe_staking_contract
import contracts.doe_nft_staking_contract as doe_nft_staking_contract
import contracts.nft_contract as nft_contract
import contracts.hidden_details as hidden_details

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

w3_arb = Web3(Web3.HTTPProvider(hidden_details.arbirum_mainnet))
w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))

arbitrum = get_arbitrum_worth(w3_arb, hidden_details.user_wallet)
doe_doe = get_doe_doe(w3_eth, hidden_details.user_wallet)
doe_nft = get_doe_nft(w3_eth, hidden_details.user_wallet)
nft = get_nft(w3_eth, hidden_details.user_wallet)

arb_doe_total = arbitrum['SLP_DOE'] + arbitrum['SLP_rewards']
doe_doe_total = doe_doe['Staked'] + doe_doe['Rewards']
doe_nft_total = doe_nft['Rewards']
nfts_total = [*doe_nft['StakedNFTs'], *nft['walletInventory']]

print(f"DOE:DOE Staked:  {doe_doe['Staked']: 10.2f} DOE")
print(f"DOE:DOE Rewards: {doe_doe['Rewards']: 10.2f} DOE")
print(f"DOE:DOE Total:   {doe_doe_total: 10.2f} DOE")
print(f"SLP:             {arbitrum['SLP_ETH']: 10.2f} ETH")
print(f"SLP:             {arbitrum['SLP_DOE']: 10.2f} DOE")
print(f"SLP:DOE Rewards: {arbitrum['SLP_rewards']: 10.2f} DOE")
print(f"Arbitrum Total:  {arb_doe_total: 10.2f} DOE")
print(f"DOE:NFT Rewards: {doe_nft_total: 10.2f} DOE")
print(f"NFT staked:   {doe_nft['StakedNFTs']}: {len(doe_nft['StakedNFTs'])}")
print(f"NFT unstaked: {nft['walletInventory']}: {len(nft['walletInventory'])}")

grand_total = arb_doe_total + doe_doe_total + doe_nft_total
print("=====================================================================")
print(f"NFTs total: {nfts_total}: {len(nfts_total)}")
print('Grand total: {:,.2f} DOE'.format(grand_total))