#!/usr/bin/python3

from brownie import config, accounts, Contract, interface, ZERO_ADDRESS
from brownie.convert import to_bytes

config['autofetch_sources'] = True

USD_AMOUNT = 10000
EUR_AMOUNT = 100
ETH_AMOUNT = 100
BTC_AMOUNT = 100
LINK_AMOUNT = 100

ADDRESS = accounts[0].address


class _MintableTestToken(Contract):
    wrapped = "0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83"

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address == self.wrapped:
            # Wrapped Fantom, send from SpookySwap
            self.transfer(target, amount, {"from": "0x2a651563c9d3af67ae0388a5c8f89b867038089e"})
        elif self.address.lower() == "0x27e611fd27b276acbd5ffd632e5eaebec9761e40".lower():  # 2pool LP
            amount = amount // 10 ** 18
            DAI = _MintableTestToken("0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e", "AnyswapERC20")
            USDC = _MintableTestToken("0x04068da6c83afcfa0e13ba15a6696662335d5b75", "AnyswapERC20")
            DAI._mint_for_testing(ADDRESS, (amount // 2) * 10 ** 18)
            USDC._mint_for_testing(ADDRESS, (amount // 2) * 10 ** 6)

            pool_address = "0x27e611fd27b276acbd5ffd632e5eaebec9761e40"
            DAI.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})
            USDC.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})

            pool_abi = getattr(interface, "CurveRenPool").abi
            pool = Contract.from_abi("CurveRenPool", pool_address, pool_abi)
            pool.add_liquidity([(amount // 2) * 10 ** 18, (amount // 2) * 10 ** 6], 0, {'from': ADDRESS})
        elif hasattr(self, "Swapin"):  # AnyswapERC20
            tx_hash = to_bytes("0x4475636b204475636b20476f6f7365")
            self.Swapin(tx_hash, target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


def _mint_wrapped(pool_address, lp_address, lp_amount):
    lp_token = _MintableTestToken(lp_address, "CurveLpTokenV5")
    lp_token._mint_for_testing(ADDRESS, lp_amount)
    pool_abi = getattr(interface, "CurvePool").abi
    pool = Contract.from_abi("CurvePool", pool_address, pool_abi)
    pool.remove_liquidity(lp_amount, [0, 0, 0], {'from': ADDRESS})


def main():
    DAI = _MintableTestToken("0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e", "AnyswapERC20")
    USDC = _MintableTestToken("0x04068da6c83afcfa0e13ba15a6696662335d5b75", "AnyswapERC20")
    fUSDT = _MintableTestToken("0x049d68029688eAbF473097a2fC38ef61633A3C7A", "AnyswapERC20")
    BTC = _MintableTestToken("0x321162Cd933E2Be498Cd2267a90534A804051b11", "AnyswapERC20")
    ETH = _MintableTestToken("0x74b23882a30290451A17c44f4F05243b6b58C76d", "AnyswapERC20")
    renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")

    _2crv = _MintableTestToken("0x27e611fd27b276acbd5ffd632e5eaebec9761e40", "CurveLpTokenV5")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    fUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    BTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    ETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)

    # Wrapped
    ib_pool_address = '0x4FC8D635c3cB1d0aa123859e2B2587d0FF2707b1'
    ib_token_address = '0xDf38ec60c0eC001142a33eAa039e49E9b84E64ED'
    _mint_wrapped(ib_pool_address, ib_token_address, 3 * USD_AMOUNT * 10 ** 18)  # iDAI, iUSDC, ifUSDT

    geist_pool_address = '0x0fa949783947Bf6c1b171DB13AEACBB488845B3f'
    geist_token_address = '0xD02a30d33153877BC20e5721ee53DeDEE0422B2F'
    _mint_wrapped(geist_pool_address, geist_token_address, 3 * USD_AMOUNT * 10 ** 18)  # gDAI, gUSDC, gfUSDT

    # Meta
    _2crv._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
