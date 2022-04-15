from web3 import Web3
import contracts.doe_nft_staking_contract as doe_nft_staking_contract
import hidden_details as hidden_details

uint128Max = 340282366920938463463374607431768211455 # 2**128 - 1
w3 = Web3(Web3.HTTPProvider(hidden_details.eth_mainnet))
print(f"Connected to Web3: {w3.isConnected()}")

data = doe_nft_staking_contract.get_data(w3, hidden_details.user_wallet)

rewardPerTokenPending = data['userRewardPerTokenPaid'] - data['rewardPerToken']
if (rewardPerTokenPending < 0):
    rewardPerTokenPending = rewardPerTokenPending + uint128Max

secondsLeft = (rewardPerTokenPending / data['rewardRate']) * data['totalSupply']
fullCycleInDays = (uint128Max / data['rewardRate']) * data['totalSupply'] / (60*60*24)
print(f"Earned:     {data['earned']} DOE")
print(f"Full cycle: {fullCycleInDays} days, with {data['totalSupply']} NTFs staked")
print(f"Cycle left: {secondsLeft} s")
print(f"Cycle left: {secondsLeft / (60*60)} h")
print(f"Cycle left: {secondsLeft / (60*60*24)} days")
