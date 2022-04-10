from web3 import Web3
import contracts.slp_doe_staking_contract as slp_doe_staking_contract
import contracts.slp_eth_doe_contract as slp_eth_doe_contract
import contracts.hidden_details as hidden_details

w3 = Web3(Web3.HTTPProvider(hidden_details.arbirum_mainnet))
print(f"Connected to Web3: {w3.isConnected()}")

balance = slp_doe_staking_contract.get_balances(w3, hidden_details.user_wallet)
slp_data = slp_eth_doe_contract.get_data(w3, hidden_details.user_wallet)

mySlpSupply = balance['Staked']  + slp_data['liquidity']
mySupplyPer = mySlpSupply / slp_data['totalSupply']


print("")
print(f"My supply: {mySlpSupply} SLP")
print(f"My supply: {mySupplyPer * 100} %")
print(f"My supply: {mySupplyPer * slp_data['reserves']['ETH']} ETH")
print(f"My supply: {mySupplyPer * slp_data['reserves']['DOE']} DOE")
print(f"Rewards:   {balance['Rewards']} DOE")

