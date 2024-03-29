#!/usr/bin/python3

from brownie import config, accounts, Contract, interface
from brownie.convert import to_bytes

config['autofetch_sources'] = True

SDT_AMOUNT = 100000
USD_AMOUNT = 10000
EUR_AMOUNT = 100
ETH_AMOUNT = 100
BTC_AMOUNT = 100
LINK_AMOUNT = 100

ADDRESS = accounts[0].address


class _MintableTestToken(Contract):
    WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi("PolygonToken", address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.WMATIC.lower():  # WMATIC
            self.transfer(target, amount, {"from": "0xadbf1854e5883eb8aa7baf50705338739e558e5b"})
        elif hasattr(self, "getRoleMember"):  # BridgeToken
            role = "0x8f4f2da22e8ac8f11e15f9fc141cddbb5deea8800186560abb6e68c5496619a9"
            minter = self.getRoleMember(role, 0)
            amount = to_bytes(amount, "bytes32")
            self.deposit(target, amount, {"from": minter})
        elif hasattr(self, "POOL"):  # AToken
            token = _MintableTestToken(self.UNDERLYING_ASSET_ADDRESS(), "BridgeToken")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "set_minter"):  # CurveLpToken
            pool = interface.CurvePool(self.minter())

            amDAI = _MintableTestToken(pool.coins(0), "AToken")
            amUSDC = _MintableTestToken(pool.coins(1), "AToken")
            amUSDT = _MintableTestToken(pool.coins(2), "AToken")

            amounts = [int(amount / 3), int(amount / 10**12 / 3), int(amount / 10**12 / 3)]

            amDAI._mint_for_testing(target, amounts[0])
            amUSDC._mint_for_testing(target, amounts[1])
            amUSDT._mint_for_testing(target, amounts[2])

            amDAI.approve(pool, amounts[0], {"from": target})
            amUSDC.approve(pool, amounts[1], {"from": target})
            amUSDT.approve(pool, amounts[2], {"from": target})

            pool.add_liquidity(amounts, 0, {"from": target})
        elif hasattr(self, "mint"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        else:
            raise ValueError("Unsupported Token")


def main():
    CRV = _MintableTestToken("0x172370d5cd63279efa6d502dab29171933a610af", "BridgeToken")
    DAI = _MintableTestToken("0x8f3cf7ad23cd3cadbd9735aff958023239c6a063", "BridgeToken")
    USDC = _MintableTestToken("0x2791bca1f2de4661ed88a30c99a7a9449aa84174", "BridgeToken")
    USDT = _MintableTestToken("0xc2132d05d31c914a87c6611c10748aeb04b58e8f", "BridgeToken")
    EURT = _MintableTestToken("0x7BDF330f423Ea880FF95fC41A280fD5eCFD3D09f", "BridgeToken")
    WETH = _MintableTestToken("0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619", "BridgeToken")
    WBTC = _MintableTestToken("0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6", "BridgeToken")
    renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")
    EURS = _MintableTestToken("0xe111178a87a3bff0c8d18decba5798827539ae99", "BridgeToken")
    WMATIC = _MintableTestToken("0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270", "WETH")
    SDT = _MintableTestToken("0x361a5a4993493ce00f61c32d4ecca5512b82ce90", "BridgeToken")

    # Wrapped
    amDAI = _MintableTestToken("0x27F8D03b3a2196956ED754baDc28D73be8830A6e", "AToken")
    amUSDC = _MintableTestToken("0x1a13F4Ca1d028320A707D99520AbFefca3998b7F", "AToken")
    amUSDT = _MintableTestToken("0x60D55F02A771d515e077c9C2403a1ef324885CeC", "AToken")
    amWBTC = _MintableTestToken("0x5c2ed810328349100A66B82b78a1791B101C9D61", "AToken")

    # Meta
    am3Crv = _MintableTestToken("0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171", "CurveLpToken")

    # ------------------------------------------------------------------------------

    CRV._mint_for_testing(ADDRESS, 100000 * 10 ** 18)
    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # EURT._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 6)
    WETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # EURS._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 2)
    WMATIC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    SDT._mint_for_testing(ADDRESS, SDT_AMOUNT * 10 ** 18)

    # Wrapped
    # amDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # amUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # amUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # amWBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)

    # Meta
    # am3Crv._mint_for_testing(ADDRESS, 100000 * 10 ** 18)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
