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


#############################################################
wallet = hidden_details.whale
#############################################################

w3_eth = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))

collection_stats = nft_data.get_collection_stats()
estimated = nft_data.get_estimated_price(891, collection_stats)

print(json.dumps(estimated, indent=3))
