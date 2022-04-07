from web3 import Web3
import doe_nft_abi
import hidden_details

uint128Max = 340282366920938463463374607431768211455 # 2**128 - 1
rewardRate = 102341260021419944000000000000000000 # = 102341260021419944*1e18

w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{hidden_details.api_key}"))
print(f"Connected to Web3: {w3.isConnected()}")

doe_nft_address = "0x5B586BFE6C283FB4020dDdbf1F0A08Fd99665819"
contract = w3.eth.contract(address=doe_nft_address, abi=doe_nft_abi.get_abi())

# Contract interaction
totalSupply = contract.functions.totalSupply().call()
userRewardPerTokenPaid = contract.functions.userRewards(hidden_details.user_wallet).call()[0]
earned = contract.functions.earned(hidden_details.user_wallet).call()
rewardPerToken = contract.functions.rewardPerToken().call()

rewardPerTokenPending = userRewardPerTokenPaid - rewardPerToken
if (rewardPerTokenPending < 0):
    rewardPerTokenPending = rewardPerTokenPending + uint128Max

secondsLeft = (rewardPerTokenPending / rewardRate) * totalSupply
fullCycleInDays = (uint128Max / rewardRate) * totalSupply / (60*60*24)
print(f"Earned:     {earned/10**18} DOE")
print(f"Full cycle: {fullCycleInDays} days, with {totalSupply} NTFs staked")
print(f"Cycle left: {secondsLeft} s")
print(f"Cycle left: {secondsLeft / (60*60)} h")
print(f"Cycle left: {secondsLeft / (60*60*24)} days")
