#!/usr/bin/python3

from brownie import config, accounts, Contract
from brownie_tokens import ERC20, MintableForkToken

config['autofetch_sources'] = True

USD_AMOUNT = 10000
EUR_AMOUNT = 100
ETH_AMOUNT = 100
BTC_AMOUNT = 100
LINK_AMOUNT = 100
CRV_AMOUNT = 100

ADDRESS = accounts[0].address


def main():
    # --- Factory plain pools ---

    # ibEUR+sEUR
    ibEUR = MintableForkToken("0x96e61422b6a9ba0e068b6c5add4ffabc6a4aae27")
    sEUR = MintableForkToken("0xD71eCFF9342A5Ced620049e616c5035F1dB98620")

    # D3
    FRAX = MintableForkToken("0x853d955acef822db058eb8505911ed77f175b99e")
    FEI = MintableForkToken("0x956f47f50a910163d8bf957cf5846d573e7f87ca")
    alUSD = MintableForkToken("0xBC6DA0FE9aD5f3b0d58160288917AA56653660E9")

    # crvCRV
    CRV = MintableForkToken("0xD533a949740bb3306d119CC777fa900bA034cd52")
    yvBOOST = MintableForkToken("0x9d409a0a012cfba9b15f6d4b36ac57a46966ab9a")
    cvxCRV = MintableForkToken("0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7")
    sCRV = MintableForkToken("0xd38aeb759891882e78e957c80656572503d8c1b1")

    # --- Factory base pools ---

    # 3pool
    DAI = MintableForkToken("0x6b175474e89094c44da98b954eedeac495271d0f")
    USDC = MintableForkToken("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
    USDT = MintableForkToken("0xdac17f958d2ee523a2206206994597c13d831ec7")
    _3Crv = MintableForkToken("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490")

    # fraxusdc
    crvFRAX = MintableForkToken("0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC")

    # sbtc
    renBTC = MintableForkToken("0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D")
    WBTC = MintableForkToken("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")
    sBTC = MintableForkToken("0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6")
    sbtcCrv = MintableForkToken("0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3")

    # --- Factory meta pools ---

    # baoUSD-3CRV
    BaoUSD = MintableForkToken("0x7945b0a6674b175695e5d1d08ae1e6f13744abb0")

    # ELONXSWAP3CRV
    ELONX = MintableForkToken("0x815b4ce34fac32b951bd26ea85901e3b834204b6")

    # ibbtc/sbtcCRV
    wibBTC = MintableForkToken("0x8751d4196027d4e6da63716fa7786b5174f04c15")

    # --- Factory crypto pools ---

    # YFIETH-fV2
    WETH = MintableForkToken("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    YFI = MintableForkToken("0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e")

    # BADGERWBTC-fV2
    BADGER = MintableForkToken("0x3472a5a71965499acd81997a54bba8d852c6e53d")

    # --- Factory crypto meta pools ---

    # DCHF/3CRV (factory-crypto-116)
    DCHF = MintableForkToken("0x045da4bfe02b320f4403674b3b7d121737727a36")

    # ------------------------------------------------------------------------------

    # # --- Factory plain pools ---
    #
    # # ibEUR+sEUR
    # ibEUR._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 18)
    # sEUR._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 18)
    #
    # # D3
    # FRAX._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # FEI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # alUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    #
    # # crvCRV
    # CRV._mint_for_testing(ADDRESS, CRV_AMOUNT * 10 ** 18)
    # yvBOOST._mint_for_testing(ADDRESS, CRV_AMOUNT * 10 ** 18)
    # cvxCRV._mint_for_testing(ADDRESS, CRV_AMOUNT * 10 ** 18)
    # # sCRV._mint_for_testing(ADDRESS, CRV_AMOUNT * 10 ** 18) Can't mint
    #
    # --- Factory base pools ---

    # 3pool
    DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    _3Crv._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # fraxusdc
    FRAX._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    crvFRAX._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # # sbtc
    # renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # sBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # sbtcCrv._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    #
    # # --- Factory meta pools ---
    #
    # # baoUSD-3CRV
    # BaoUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    #
    # # ELONXSWAP3CRV
    # ELONX._mint_for_testing(ADDRESS, USD_AMOUNT)
    #
    # # ibbtc/sbtcCRV
    # wibBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    #
    # # --- Factory crypto pools ---
    #
    # # YFIETH-fV2
    # WETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    # YFI._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    #
    # # BADGERWBTC-fV2
    # BADGER._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)

    # --- Factory crypto meta pools ---

    # DCHF/3CRV (factory-crypto-116)
    DCHF._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)

    # cvxCrv/FraxBP (factory-crypto-97)
    cvxCRV._mint_for_testing(ADDRESS, CRV_AMOUNT * 10 ** 18)


if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
