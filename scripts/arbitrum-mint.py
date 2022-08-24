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
    wrapped = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address == self.wrapped:  # WETH
            self.transfer(target, amount, {"from": "0x0c1cf6883efa1b496b01f654e247b9b419873054"})
        elif hasattr(self, "bridgeMint"):  # ArbitrumERC20
            self.bridgeMint(target, amount, {"from": self.l2Gateway()})
        elif hasattr(self, "POOL"):  # AToken
            token = _MintableTestToken(self.UNDERLYING_ASSET_ADDRESS(), "ArbitrumERC20")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


def _mint_2crv_and_usdc(amount):
    USDT = _MintableTestToken("0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", "ArbitrumERC20")
    USDT._mint_for_testing(ADDRESS, amount * 10 ** 6)

    pool_address = "0x7f90122bf0700f9e7e1f688fe926940e8839f353"
    USDT.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})

    pool_abi = getattr(interface, "CurveRenPool").abi
    pool = Contract.from_abi("CurveRenPool", pool_address, pool_abi)
    pool.add_liquidity([0, amount * 10 ** 6], 0, {'from': ADDRESS})  # mint 2CRV
    pool.remove_liquidity_one_coin(amount // 2 * 10 ** 18, 0, 0, {'from': ADDRESS})  # mint USDC


def _mint_deETH(address):
    pool_abi = getattr(interface, "CurveRenPool").abi
    pool = Contract.from_abi("CurveRenPool", "0x0a824b5d4c96ea0ec46306efbd34bf88fe1277e0", pool_abi)

    pool.exchange(0, 1, 50 * 10 ** 18, 0, {"from": address, "value": 50 * 10 ** 18})


def _mint_aArbDAI(aarbusdt_amount):
    aArbUSDT = _MintableTestToken("0x6ab707aca953edaefbc4fd23ba73294241490620", "AToken")
    pool_address = "0x37c9be6c81990398e9b87494484afc6a4608c25d"  # Aave aDAI+aUSC+aUSDT USDFACTORY
    lp_token = _MintableTestToken("0x37c9be6c81990398e9b87494484afc6a4608c25d", "CurveLpTokenV5")

    aArbUSDT.approve(pool_address, 2 ** 256 - 1, {'from': ADDRESS})
    pool_abi = getattr(interface, "CurvePool").abi
    pool = Contract.from_abi("CurvePool", pool_address, pool_abi)
    pool.add_liquidity([0, 0, aarbusdt_amount * 10 ** 6], 0, {'from': ADDRESS})  # mint LP
    lp_amount = lp_token.balanceOf(ADDRESS)
    pool.remove_liquidity_one_coin(lp_amount, 0, 0, {'from': ADDRESS})  # mint DAI


def main():
    WETH = _MintableTestToken("0x82aF49447D8a07e3bd95BD0d56f35241523fBab1", "WETH")
    USDT = _MintableTestToken("0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9", "ArbitrumERC20")
    WBTC = _MintableTestToken("0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f", "ArbitrumERC20")
    renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")
    EURS = _MintableTestToken("0xd22a58f79e9481d1a88e00c343885a588b34b68b", "renERC20")

    # --- FACTORY ---

    MIM = _MintableTestToken("0xfea7a6a0b346362bf88a9e4a88416b77a57d6c2a", "renERC20")
    aArbUSDC = _MintableTestToken("0x625e7708f30ca75bfd92586e17077590c60eb4cd", "AToken")
    aArbUSDT = _MintableTestToken("0x6ab707aca953edaefbc4fd23ba73294241490620", "AToken")

    # ------------------------------------------------------------------------------

    WETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    USDT._mint_for_testing(ADDRESS, 3 * USD_AMOUNT * 10 ** 6)
    WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    EURS._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 2)

    # Meta
    _mint_2crv_and_usdc(USD_AMOUNT * 2)

    # --- FACTORY ---

    # MIM (factory-v2-0)
    MIM._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # deBridge-ETH (factory-v2-15)
    _mint_deETH(ADDRESS)

    # Aave aDAI+aUSC+aUSDT USDFACTORY (factory-v2-29)
    aArbUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    aArbUSDT._mint_for_testing(ADDRESS, 2 * USD_AMOUNT * 10 ** 6)
    _mint_aArbDAI(USD_AMOUNT)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "50 ether")
