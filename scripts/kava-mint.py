#!/usr/bin/python3

from brownie import config, accounts, Contract, interface, ZERO_ADDRESS

config['autofetch_sources'] = True


ADDRESS = accounts[0].address


class _MintableTestToken(Contract):

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        self.transfer(target, amount, {"from": "0x62bf12869E145A862218eE7e28F942Cc7FaeC460"})

def main():
    DAI = _MintableTestToken("0x765277EebeCA2e31912C9946eAe1021199B39C61", "ERC20")
    USDC = _MintableTestToken("0xfA9343C3897324496A05fC75abeD6bAC29f8A40f", "ERC20")
    USDT = _MintableTestToken("0xB44a9B6905aF7c801311e8F4E76932ee959c663C", "ERC20")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, 10000 * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, 10000 * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, 10000 * 10 ** 6)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
