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
        self.transfer(target, amount, {"from": "0xCdF46720BdF30D6bd0912162677c865d4344B0CA"})


def main():
    DAI = _MintableTestToken("0xe3520349F477A5F6EB06107066048508498A291b", "ERC20")
    USDC = _MintableTestToken("0xB12BFcA5A55806AaF64E99521918A4bf0fC40802", "ERC20")
    USDT = _MintableTestToken("0x4988a896b1227218e4A686fdE5EabdcAbd91571f", "ERC20")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, 10000 * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, 10000 * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, 10000 * 10 ** 6)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
