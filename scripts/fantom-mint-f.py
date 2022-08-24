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
        elif hasattr(self, "Swapin"):  # AnyswapERC20
            tx_hash = to_bytes("0x4475636b204475636b20476f6f7365")
            self.Swapin(tx_hash, target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


def _mint_2pool(amount):
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


def _mint_by_swap(pool_address, token_to_swap, address, amount, i, j):
    pool_abi = getattr(interface, "CurveRenPool").abi
    pool = Contract.from_abi("CurveRenPool", pool_address, pool_abi)

    allowance = token_to_swap.allowance(address, pool_address)
    if allowance < amount:
        token_to_swap.approve(pool_address, 2 ** 256 - 1, {"from": address})

    pool.exchange(i, j, amount, 0, {"from": address})


def _mint_wrapped(pool_address, lp_address, lp_amount):
    lp_token = _MintableTestToken(lp_address, "CurveLpTokenV5")
    lp_token._mint_for_testing(ADDRESS, lp_amount)
    pool_abi = getattr(interface, "CurvePool").abi
    pool = Contract.from_abi("CurvePool", pool_address, pool_abi)
    pool.remove_liquidity(lp_amount, [0, 0, 0], {'from': ADDRESS})


def main():
    MIM = _MintableTestToken("0x82f0b8b456c1a451378467398982d4834b6829c1", "AnyswapERC20")
    DAI = _MintableTestToken("0x8d11ec38a3eb5e956b052f67da8bdc9bef8abf3e", "AnyswapERC20")
    USDC = _MintableTestToken("0x04068da6c83afcfa0e13ba15a6696662335d5b75", "AnyswapERC20")
    fUSDT = _MintableTestToken("0x049d68029688eAbF473097a2fC38ef61633A3C7A", "AnyswapERC20")
    axlUSDC = _MintableTestToken("0x1b6382dbdea11d97f24495c9a90b7c88469134a4", "renERC20")
    # FRAX = _MintableTestToken("0xdc301622e621166bd8e82f2ca0a26c13ad0be355", "CurveLpTokenV5")
    _2crv = _MintableTestToken("0x27e611fd27b276acbd5ffd632e5eaebec9761e40", "CurveLpTokenV5")
    g3CRV = _MintableTestToken("0xd02a30d33153877bc20e5721ee53dedee0422b2f", "CurveLpTokenV5")
    aCRV = _MintableTestToken("0x666a3776b3e82f171cb1dff7428b6808d2cd7d02", "AnyswapERC20")
    CRV = _MintableTestToken("0x1e4f97b9f9f913c46f1632781732927b9019c68b", "AnyswapERC20")

    BTC = _MintableTestToken("0x321162Cd933E2Be498Cd2267a90534A804051b11", "AnyswapERC20")
    ETH = _MintableTestToken("0x74b23882a30290451A17c44f4F05243b6b58C76d", "AnyswapERC20")
    renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")

    # ------------------------------------------------------------------------------

    # 3poolV2 (factory-v2-1)
    MIM._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    fUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)

    # 4pool (factory-v2-7)
    # # fUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # # USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # # MIM._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # axlUSDC/USDC (factory-v2-85)
    axlUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # # USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)

    # FRAX2pool (factory-v2-16)
    _mint_2pool(USD_AMOUNT * 2)
    FRAX2pool_address = "0x7a656b342e14f745e2b164890e88017e27ae7320"
    _mint_by_swap(FRAX2pool_address, _2crv, ADDRESS, USD_AMOUNT * 10 ** 18, 1, 0)  # FRAX

    # Geist Frax (factory-v2-40)
    # # FRAX._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    g3CRV._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # aCRV/CRV (factory-crypto-3)
    aCRV._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    CRV._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # CRYPTO
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


    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
