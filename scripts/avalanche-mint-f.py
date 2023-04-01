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
    WAVAX = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"
    USDCT = ["0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E".lower(), "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7".lower()]

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.WAVAX.lower():  # WAVAX
            # Wrapped Avax, send from Iron Bank
            self.transfer(target, amount, {"from": "0xb3c68d69e95b095ab4b33b4cb67dbc0fbf3edf56"})
        elif self.address.lower() in self.USDCT:  # USDC, USDt
            self.transfer(target, amount, {"from": "0x9f8c163cba728e99993abe7495f06c0a3c8ac8b9"})  # Binance: C-Chain Hot Wallet
        elif hasattr(self, "POOL"):  # AToken
            token = _MintableTestToken(self.UNDERLYING_ASSET_ADDRESS(), "AvalancheERC20")
            lending_pool = interface.AaveLendingPool(self.POOL())
            token._mint_for_testing(target, amount)
            token.approve(lending_pool, amount, {"from": target})
            lending_pool.deposit(token, amount, target, 0, {"from": target})
        elif hasattr(self, "mint") and hasattr(self, "owner"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        elif hasattr(self, "mint") and hasattr(self, "minter"):  # Curve LP Token
            self.mint(target, amount, {"from": self.minter()})
        elif hasattr(self, "mint"):  # AvalancheERC20 (bridge token)
            self.mint(target, amount, ZERO_ADDRESS, 0, 0x0, {"from": "0xEb1bB70123B2f43419d070d7fDE5618971cc2F8f"})
        else:
            raise ValueError("Unsupported Token")


def _mint_by_swap(pool_address, token_to_swap, address, amount, i, j):
    pool = Contract(pool_address)

    allowance = token_to_swap.allowance(address, pool_address)
    if allowance < amount:
        token_to_swap.approve(pool_address, 2 ** 256 - 1, {"from": address})

    pool.exchange(i, j, amount, 0, {"from": address})


def main():
    DAIe = _MintableTestToken("0xd586E7F844cEa2F87f50152665BCbc2C279D8d70", "AvalancheERC20")
    USDCe = _MintableTestToken("0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664", "AvalancheERC20")
    USDTe = _MintableTestToken("0xc7198437980c041c805A1EDcbA50c1Ce5db95118", "AvalancheERC20")

    # Meta
    av3Crv = _MintableTestToken("0x1337BedC9D22ecbe766dF105c9623922A27963EC", "CurveLpTokenV5")

    # Factory
    # MIM = _MintableTestToken("0x130966628846bfd36ff31a822705796e8cb8c18d", "CurveLpTokenV5")
    USDC = _MintableTestToken("0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e", "AvalancheERC20")


    # ------------------------------------------------------------------------------

    DAIe._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDCe._mint_for_testing(ADDRESS, 2 * USD_AMOUNT * 10 ** 6)
    USDTe._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)

    # Meta
    av3Crv._mint_for_testing(ADDRESS, 10 * USD_AMOUNT * 10 ** 18)

    # Factory
    mim_pool_address = "0x30df229cefa463e991e29d42db0bae2e122b2ac7"
    _mint_by_swap(mim_pool_address, av3Crv, ADDRESS, USD_AMOUNT * 10 ** 18, 1, 0)  # MIM
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)


    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
