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

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address.lower() == self.WAVAX.lower():  # WAVAX
            # Wrapped Avax, send from Iron Bank
            self.transfer(target, amount, {"from": "0xb3c68d69e95b095ab4b33b4cb67dbc0fbf3edf56"})
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


def main():
    DAI = _MintableTestToken("0xd586E7F844cEa2F87f50152665BCbc2C279D8d70", "AvalancheERC20")
    USDC = _MintableTestToken("0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664", "AvalancheERC20")
    USDT = _MintableTestToken("0xc7198437980c041c805A1EDcbA50c1Ce5db95118", "AvalancheERC20")
    WETH = _MintableTestToken("0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB", "AvalancheERC20")
    WBTC = _MintableTestToken("0x50b7545627a5162F82A992c33b87aDc75187B218", "AvalancheERC20")
    renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")

    # Wrapped
    avDAI = _MintableTestToken("0x47AFa96Cdc9fAb46904A55a6ad4bf6660B53c38a", "AToken")
    avUSDC = _MintableTestToken("0x46A51127C3ce23fb7AB1DE06226147F446e4a857", "AToken")
    avUSDT = _MintableTestToken("0x532E6537FEA298397212F09A61e03311686f548e", "AToken")
    avWBTC = _MintableTestToken("0x686bEF2417b6Dc32C50a3cBfbCC3bb60E1e9a15D", "AToken")

    # Meta
    av3Crv = _MintableTestToken("0x1337BedC9D22ecbe766dF105c9623922A27963EC", "CurveLpTokenV5")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    WETH._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)

    # Wrapped
    avDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    avUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    avUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    avWBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)

    # Meta
    av3Crv._mint_for_testing(ADDRESS, 100000 * 10 ** 18)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
