from web3 import Web3
import contracts.doe_nft_abi as doe_nft_abi


def get_data(w3, wallet):
    contract_address = "0x5B586BFE6C283FB4020dDdbf1F0A08Fd99665819"
    contract = w3.eth.contract(address=contract_address, abi=doe_nft_abi.get_abi())
    totalSupply = contract.functions.totalSupply().call()
    userRewardPerTokenPaid = contract.functions.userRewards(wallet).call()[0]
    earned = Web3.fromWei(contract.functions.earned(wallet).call(), "ether")
    rewardPerToken = contract.functions.rewardPerToken().call()

    return {
        "rewardRate": 102341260021419944000000000000000000, # = 102341260021419944*1e18
        "totalSupply": totalSupply,
        "userRewardPerTokenPaid": userRewardPerTokenPaid,
        "earned": earned,
        "rewardPerToken": rewardPerToken,
    }
