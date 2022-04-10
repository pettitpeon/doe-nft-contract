from web3 import Web3
import contracts.nft_abi as nft_abi


def get_data(w3, wallet):
    contract_address = "0xD8CDB4b17a741DC7c6A57A650974CD2Eba544Ff7"
    contract = w3.eth.contract(address=contract_address, abi=nft_abi.get_abi())
    balanceOf = contract.functions.balanceOf(wallet).call()
    walletInventory = contract.functions.walletInventory(wallet).call()


    return {
        "balanceOf": balanceOf,
        "walletInventory": walletInventory,
    }
