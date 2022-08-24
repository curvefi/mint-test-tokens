#!/usr/bin/python3

from brownie import config, accounts, Contract, interface
from brownie.convert import to_bytes

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
        self.from_abi("PolygonToken", address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if hasattr(self, "getRoleMember"):  # BridgeToken
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
            if self.address == "0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171":
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
            else:
                pool = interface.CurveRenPool(self.minter())

                amWBTC = _MintableTestToken("0x5c2ed810328349100A66B82b78a1791B101C9D61", "AToken")
                renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")

                amounts = [int(amount / 10 ** 10 / 2), int(amount / 10 ** 10 / 2)]

                amWBTC._mint_for_testing(target, amounts[0])
                renBTC._mint_for_testing(target, amounts[1])

                amWBTC.approve(pool, amounts[0], {"from": target})
                renBTC.approve(pool, amounts[1], {"from": target})

                pool.add_liquidity(amounts, 0, {"from": target})
        elif hasattr(self, "mint"):  # renERC20
            self.mint(target, amount, {"from": self.owner()})
        else:
            raise ValueError("Unsupported Token")


def mint_by_swap(pool_address, token_to_swap, address, amount, i, j):
    pool = Contract(pool_address)

    allowance = token_to_swap.allowance(address, pool_address)
    if allowance < amount:
        token_to_swap.approve(pool_address, 2 ** 256 - 1, {"from": address})

    pool.exchange(i, j, amount, 0, {"from": address})


def main():
    # --- Factory plain pools ---

    # CRVALRTO
    CRV = _MintableTestToken("0x172370d5cd63279efa6d502dab29171933a610af", "BridgeToken")

    # 3EUR + 4eur-2
    EURT = _MintableTestToken("0x7BDF330f423Ea880FF95fC41A280fD5eCFD3D09f", "BridgeToken")

    # --- Factory base pools ---

    # aave
    DAI = _MintableTestToken("0x8f3cf7ad23cd3cadbd9735aff958023239c6a063", "BridgeToken")
    USDC = _MintableTestToken("0x2791bca1f2de4661ed88a30c99a7a9449aa84174", "BridgeToken")
    USDT = _MintableTestToken("0xc2132d05d31c914a87c6611c10748aeb04b58e8f", "BridgeToken")
    am3Crv =_MintableTestToken("0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171", "CurveLpToken")

    # ren
    WBTC = _MintableTestToken("0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6", "BridgeToken")
    renBTC = _MintableTestToken("0xDBf31dF14B66535aF65AaC99C32e9eA844e14501", "renERC20")
    btcCRV = _MintableTestToken("0xf8a57c1d3b9629b77b6726a042ca48990A84Fb49", "CurveLpToken")

    # ------------------------------------------------------------------------------

    # --- Factory plain pools ---

    # CRVALRTO
    CRV._mint_for_testing(ADDRESS, 2 * USD_AMOUNT * 10 ** 18)
    crvalrto_address = "0x8914b29f7bea602a183e89d6843ecb251d56d07e"
    mint_by_swap(crvalrto_address, CRV, ADDRESS, USD_AMOUNT * 10 ** 18, 0, 1)  # ALRTO

    # 3EUR + 4eur-2
    EURT._mint_for_testing(ADDRESS, 7 * EUR_AMOUNT * 10 ** 6)
    _4eur_address = "0xad326c253a84e9805559b73a08724e11e49ca651"
    mint_by_swap(_4eur_address, EURT, ADDRESS, 2 * EUR_AMOUNT * 10 ** 6, 3, 0)  # jEUR
    mint_by_swap(_4eur_address, EURT, ADDRESS, 2 * EUR_AMOUNT * 10 ** 6, 3, 1)  # PAR
    mint_by_swap(_4eur_address, EURT, ADDRESS, 2 * EUR_AMOUNT * 10 ** 6, 3, 2)  # EURS

    # --- Factory base pools ---

    # aave
    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    am3Crv._mint_for_testing(ADDRESS, 2 * USD_AMOUNT * 10 ** 18)

    # # ren
    # WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # btcCRV._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)

    # --- Factory meta pools ---

    # FRAX3CRV-f3CRV
    FRAX3CRVf3CRV_address = "0x5e5a23b52cb48f5e70271be83079ca5bc9c9e9ac"
    mint_by_swap(FRAX3CRVf3CRV_address, am3Crv, ADDRESS, USD_AMOUNT * 10 ** 18, 1, 0)  # FRAX

    # if ADDRESS != accounts[0].address:
    #     accounts[0].transfer(ADDRESS, "100 ether")
