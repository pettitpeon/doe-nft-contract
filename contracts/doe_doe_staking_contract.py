from web3 import Web3
import contracts.doe_doe_abi as doe_doe_abi

def get_balances(w3, wallet):
    contract_address = "0x60C6b5DC066E33801F2D9F2830595490A3086B4e"
    contract = w3.eth.contract(address=contract_address, abi=doe_doe_abi.get_abi())
    balanceOf =  Web3.fromWei(contract.functions.balanceOf(wallet).call(), "ether")
    earned = Web3.fromWei(contract.functions.earned(wallet).call(), "ether")

    return {
        "Staked": balanceOf,
        "Rewards": earned,
        }
