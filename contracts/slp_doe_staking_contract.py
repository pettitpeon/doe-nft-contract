from web3 import Web3
import contracts.slp_doe_abi as slp_doe_abi

def get_balances(w3, wallet):
    contract_address = "0x3C40601f73fbf50b81a72edbf2786f14EBb7371b"
    contract = w3.eth.contract(address=contract_address, abi=slp_doe_abi.get_abi())
    balanceOf =  Web3.fromWei(contract.functions.balanceOf(wallet).call(), "ether")
    earned = Web3.fromWei(contract.functions.earned(wallet).call(), "ether")

    return {
        "Staked": balanceOf,
        "Rewards": earned,
        }
