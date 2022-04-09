from web3 import Web3
import contracts.doe_doe_staking_contract as doe_doe_staking_contract
import contracts.hidden_details as hidden_details

uint128Max = 340282366920938463463374607431768211455 # 2**128 - 1
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{hidden_details.api_key}"))
print(f"Connected to Web3: {w3.isConnected()}")

balance = doe_doe_staking_contract.get_balances(w3, hidden_details.user_wallet)

print(f"Staked:  {balance['Staked']} DOE")
print(f"Rewards: {balance['Rewards']} DOE")
