#!/usr/bin/python3

from brownie import config, accounts, Contract, interface, ZERO_ADDRESS

config['autofetch_sources'] = True


USD_AMOUNT = 10000
EUR_AMOUNT = 100
ETH_AMOUNT = 100
BTC_AMOUNT = 100
LINK_AMOUNT = 100

ADDRESS = accounts[0].address


class _MintableTestToken(Contract):
    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1".lower():  # DAI
            self.transfer(target, amount, {"from": "0xd08cd45925132537ea241179b19ab3a33ad97f3d"})
        elif hasattr(self, "l2Bridge"):  # OptimismBridgeToken
            self.mint(target, amount, {"from": self.l2Bridge()})
        elif hasattr(self, "bridge"):  # OptimismBridgeToken2
            self.bridgeMint(target, amount, {"from": self.bridge()})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


def _mint_3crv(amount):
    USDC = _MintableTestToken("0x7f5c764cbc14f9669b88837ca1490cca17c31607", "OptimismBridgeToken")
    USDC._mint_for_testing(ADDRESS, amount * 10 ** 6)

    pool_address = "0x1337BedC9D22ecbe766dF105c9623922A27963EC"
    USDC.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})

    pool_abi = getattr(interface, "CurvePool").abi
    pool = Contract.from_abi("CurvePool", pool_address, pool_abi)
    pool.add_liquidity([0, 2 * amount * 10 ** 6, 0], 0, {'from': ADDRESS})  # mint 3CRV


def _mint_by_swap(pool_address, token_to_swap, address, amount, i, j):
    pool_abi = getattr(interface, "CurveRenPool").abi
    pool = Contract.from_abi("CurveRenPool", pool_address, pool_abi)

    allowance = token_to_swap.allowance(address, pool_address)
    if allowance < amount:
        token_to_swap.approve(pool_address, 2 ** 256 - 1, {"from": address})

    pool.exchange(i, j, amount, 0, {"from": address})


def _mint_by_swap_eth(pool_address, address, amount, i, j):
    pool_abi = getattr(interface, "CurveEthPool").abi
    pool = Contract.from_abi("CurveEthPool", pool_address, pool_abi)

    pool.exchange(i, j, amount, 0, {"from": address, "value": amount})


def main():
    DAI = _MintableTestToken("0xda10009cbd5d07dd0cecc66161fc93d7c9000da1", "OptimismBridgeToken")
    USDC = _MintableTestToken("0x7f5c764cbc14f9669b88837ca1490cca17c31607", "OptimismBridgeToken")
    USDT = _MintableTestToken("0x94b008aa00579c1307b0ef2c499ad98a8ce58e58", "OptimismBridgeToken")
    _3crv = _MintableTestToken("0x1337BedC9D22ecbe766dF105c9623922A27963EC", "CurveLpTokenV5")

    wstETH = _MintableTestToken("0x1f32b1c2345538c0c6f582fcb022739c4a194ebb", "OptimismBridgeToken2")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    _mint_3crv(USD_AMOUNT)

    wstETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)

    # --- FACTORY ---

    # sUSD Synthetix (factory-v2-0)
    susd_pool_address = "0x061b87122ed14b9526a813209c8a59a633257bab"
    _mint_by_swap(susd_pool_address, _3crv, ADDRESS, USD_AMOUNT // 2 * 10 ** 18, 1, 0)  # sUSD

    # sETH/ETH (factory-v2-10)
    seth_pool_address = "0x7bc5728bc2b59b45a58d9a576e2ffc5f0505b35e"
    _mint_by_swap_eth(seth_pool_address, ADDRESS, ETH_AMOUNT // 2 * 10 ** 18, 0, 1)  # sETH

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
