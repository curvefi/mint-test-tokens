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
    wrapped = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d".lower()

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.wrapped:  # WXDAI
            self.transfer(target, amount, {"from": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # CurveLpTokenV5
            self.mint(target, amount, {"from": self.minter()})
        else:
            raise ValueError("Unsupported Token")


def _mint_by_swap(pool_address, token_to_swap, address, amount, i, j):
    pool_abi = getattr(interface, "CurveRenPool").abi
    pool = Contract.from_abi("CurveRenPool", pool_address, pool_abi)

    allowance = token_to_swap.allowance(address, pool_address)
    if allowance < amount:
        token_to_swap.approve(pool_address, 2 ** 256 - 1, {"from": address})

    pool.exchange(i, j, amount, 0, {"from": address})


def _rug_native_token():
    for acc in accounts:
        if acc.address != ADDRESS:
            acc.transfer(ADDRESS, 99 * 10 ** 18)


def main():
    WXDAI = _MintableTestToken("0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d", "WETH")
    USDC = _MintableTestToken("0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83", "renERC20")
    USDT = _MintableTestToken("0x4ECaBa5870353805a9F068101A40E0f32ed605C6", "renERC20")
    RAI = _MintableTestToken("0xd7a28aa9c470e7e9d8c676bcd5dd2f40c5683afa", "renERC20")
    x3crv = _MintableTestToken("0x1337BedC9D22ecbe766dF105c9623922A27963EC", "CurveLpTokenV5")

    # --- FACTORY ---

    MAI = _MintableTestToken("0x3F56e0c36d275367b8C502090EDF38289b3dEa0d", "renERC20")
    GNO = _MintableTestToken("0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb", "renERC20")

    # abi = getattr(interface, "FactoryRegistry").abi
    # FACTORY = Contract.from_abi("FactoryRegistry", "0xD19Baeadc667Cf2015e395f2B08668Ef120f41F5", abi)
    # for n_coins in range(2, 5):
    #     for impl in range(4):
    #         print(FACTORY.plain_implementations(n_coins, impl))

    # ------------------------------------------------------------------------------

    WXDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    RAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    x3crv._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # --- FACTORY ---

    MAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    GNO._mint_for_testing(ADDRESS, 2 * USD_AMOUNT * 10 ** 18)
    gno_pool_address = "0xbdf4488dcf7165788d438b62b4c8a333879b7078"
    _mint_by_swap(gno_pool_address, GNO, ADDRESS, USD_AMOUNT * 10 ** 18, 1, 0)  # sGNO

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
