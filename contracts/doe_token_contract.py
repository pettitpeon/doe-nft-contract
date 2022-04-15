from web3 import Web3
import contracts.doe_token_abi as doe_token_abi


def get_main_balance(w3, wallet):
    contract_address = "0xf8E9F10c22840b613cdA05A0c5Fdb59A4d6cd7eF"
    contract = w3.eth.contract(address=contract_address, abi=doe_token_abi.get_abi())
    balanceOf = contract.functions.balanceOf(wallet).call()
    return Web3.fromWei(balanceOf, 'ether')

def get_arb_balance(w3, wallet):
    contract_address = "0xE71Db7a96daB25cDb9f4cbC7F686da02192B0E88"
    contract = w3.eth.contract(address=contract_address, abi=doe_token_abi.get_abi())
    balanceOf = contract.functions.balanceOf(wallet).call()
    return Web3.fromWei(balanceOf, 'ether')
