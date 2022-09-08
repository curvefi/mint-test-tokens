#!/usr/bin/python3

from brownie import config, accounts, Contract, interface, ZERO_ADDRESS

config['autofetch_sources'] = True


ADDRESS = accounts[0].address


class _MintableTestToken(Contract):
    xcDOT = "0xffffffff1fcacbd218edc0eba20fc2308c778080".lower()
    stDOT = "0xfa36fe1da08c89ec72ea1f0143a35bfd5daea108".lower()

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.xcDOT:
            self.transfer(target, amount, {"from": "0x6b28fb12ee41baa9d1df16971de53adde6d1be5b"})
        elif self.address.lower() == self.stDOT:
            self.transfer(target, amount, {"from": "0x99fe7c594e72e04acecf1c510d90b7c1bbf94e8a"})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


def _mint_3crv():
    DAI = _MintableTestToken("0xc234A67a4F840E61adE794be47de455361b52413", "renERC20")
    USDC = _MintableTestToken("0x8f552a71EFE5eeFc207Bf75485b356A0b3f01eC9", "renERC20")
    USDT = _MintableTestToken("0x8e70cD5B4Ff3f62659049e74b6649c6603A0E594", "renERC20")

    pool_address = "0xace58a26b8db90498ef0330fdc9c2655db0c45e2"
    DAI.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})
    USDC.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})
    USDT.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})

    pool_abi = getattr(interface, "CurvePool").abi
    pool = Contract.from_abi("CurvePool", pool_address, pool_abi)
    pool.add_liquidity([1000 * 10 ** 18, 1000 * 10 ** 6, 1000 * 10 ** 6], 0, {'from': ADDRESS})  # mint 3CRV


def main():
    DAI = _MintableTestToken("0xc234A67a4F840E61adE794be47de455361b52413", "renERC20")
    USDC = _MintableTestToken("0x8f552a71EFE5eeFc207Bf75485b356A0b3f01eC9", "renERC20")
    USDT = _MintableTestToken("0x8e70cD5B4Ff3f62659049e74b6649c6603A0E594", "renERC20")

    # --- FACTORY ---


    DAI2 = _MintableTestToken("0x765277EebeCA2e31912C9946eAe1021199B39C61", "renERC20")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, 10000 * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, 10000 * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, 10000 * 10 ** 6)
    _mint_3crv()

    # --- FACTORY ---

    DAI2._mint_for_testing(ADDRESS, 10000 * 10 ** 18)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
