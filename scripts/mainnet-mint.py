#!/usr/bin/python3

from brownie import config, accounts, Contract
from brownie_tokens import ERC20, MintableForkToken

config['autofetch_sources'] = True

USD_AMOUNT = 10000
EUR_AMOUNT = 100
ETH_AMOUNT = 100
BTC_AMOUNT = 100
LINK_AMOUNT = 100

ADDRESS = accounts[0].address


def mint_by_swap(address, token_address, proxy_token_address, proxy_token_decimals, pool_address, i, j, amount):
    proxy_token = MintableForkToken(proxy_token_address)
    pool = Contract(pool_address)

    allowance = proxy_token.allowance(accounts[0].address, pool.address)
    if allowance < amount:
        proxy_token.approve(pool.address, 2 ** 256 - 1, {"from": accounts[0].address})

    proxy_token._mint_for_testing(accounts[0].address, amount * 10 ** proxy_token_decimals)
    pool.exchange(i, j, amount * 10 ** proxy_token_decimals, 0, {"from": accounts[0].address})

    if address != accounts[0].address:
        token = Contract(token_address)
        token_balance = token.balanceOf(accounts[0].address)
        token.transfer(address, token_balance)


def main():
    CRV = MintableForkToken("0xD533a949740bb3306d119CC777fa900bA034cd52")
    CVX = MintableForkToken("0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b")
    DAI = MintableForkToken("0x6b175474e89094c44da98b954eedeac495271d0f")
    USDC = MintableForkToken("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
    USDT = MintableForkToken("0xdac17f958d2ee523a2206206994597c13d831ec7")
    sUSD = MintableForkToken("0x57Ab1ec28D129707052df4dF418D58a2D46d5f51")
    renBTC = MintableForkToken("0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D")
    WBTC = MintableForkToken("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")
    sBTC = MintableForkToken("0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6")
    HBTC = MintableForkToken("0x0316EB71485b0Ab14103307bf65a021042c6d380")
    GUSD = MintableForkToken("0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd")
    HUSD = MintableForkToken("0xdF574c24545E5FfEcb9a659c229253D4111d87e1")
    USDK = MintableForkToken("0x1c48f86ae57291F7686349F12601910BD8D470bb")
    USDN = MintableForkToken("0x674C6Ad92Fd080e4004b2312b45f796a192D27a0")
    LINKUSD = MintableForkToken("0x0E2EC54fC0B509F445631Bf4b91AB8168230C752")
    mUSD = MintableForkToken("0xe2f2a5C287993345a840Db3B0845fbC70f5935a5")
    RSV = MintableForkToken("0x196f4727526eA7FB1e17b2071B3d8eAA38486988")
    TBTC = MintableForkToken("0x8dAEBADE922dF735c38C80C7eBD708Af50815fAa")
    DUSD = MintableForkToken("0x5BC25f649fc4e26069dDF4cF4010F9f706c23831")
    pBTC = MintableForkToken("0x5228a22e72ccC52d415EcFd199F99D0665E7733b")
    BBTC = MintableForkToken("0x9be89d2a4cd102d8fecc6bf9da793be995c22541")
    oBTC = MintableForkToken("0x8064d9Ae6cDf087b1bcd5BDf3531bD5d8C537a68")
    sETH = MintableForkToken("0x5e74c9036fb86bd7ecdcb084a0673efc32ea31cb")
    EURS = MintableForkToken("0xdB25f211AB05b1c97D595516F45794528a807ad8")
    sEUR = MintableForkToken("0xD71eCFF9342A5Ced620049e616c5035F1dB98620")
    EURT = MintableForkToken("0xC581b735A1688071A1746c968e0798D642EDE491")
    UST = MintableForkToken("0xa47c8bf37f92abed4a126bda807a7b7498661acd")
    stETH = MintableForkToken("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
    aETH = MintableForkToken("0xE95A203B1a91a908F9B9CE46459d101078c2c3cb")
    USDP = MintableForkToken("0x1456688345527bE1f37E9e627DA0837D6f08C925")
    LINK = MintableForkToken("0x514910771AF9Ca656af840dff83E8264EcF986CA")
    sLINK = MintableForkToken("0xbBC455cb4F1B9e4bFC4B73970d360c8f032EfEE6")
    PAX = MintableForkToken("0x8e870d67f660d95d5be530380d0ec0bd388289e1")
    rETH = MintableForkToken("0x9559Aaa82d9649C7A7b220E7c461d2E74c9a3593")
    TUSD = MintableForkToken("0x0000000000085d4780B73119b644AE5ecd22b376")
    FRAX = MintableForkToken("0x853d955acef822db058eb8505911ed77f175b99e")
    LUSD = MintableForkToken("0x5f98805A4E8be255a32880FDeC7F6728C6568bA0")
    BUSD = MintableForkToken("0x4Fabb145d64652a948d72533023f6E7A623C7C53")
    alUSD = MintableForkToken("0xBC6DA0FE9aD5f3b0d58160288917AA56653660E9")
    MIM = MintableForkToken("0x99d8a9c45b2eca8864373a26d1459e3dff1e17f3")
    WETH = MintableForkToken("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    XAUt = MintableForkToken("0x68749665ff8d2d112fa859aa293f07a622782f38")
    SPELL = MintableForkToken("0x090185f2135308bad17527004364ebcc2d37e5f6")
    T = MintableForkToken("0xCdF7028ceAB81fA0C6971208e83fa7872994beE5")
    RAI = MintableForkToken("0x03ab458634910aad20ef5f1c8ee96f1d6ac54919")
    WormholeUST = MintableForkToken("0xa693B19d2931d498c5B318dF961919BB4aee87a5")
    EUROC = MintableForkToken("0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c")

    # Wrapped
    cDAI = MintableForkToken("0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643")
    cUSDC = MintableForkToken("0x39AA39c021dfbaE8faC545936693aC917d5E7563")
    cyDAI = MintableForkToken("0x8e595470ed749b85c6f7669de83eae304c2ec68f")
    cyUSDT = MintableForkToken("0x48759f220ed983db51fa7a8c0d2aab8f3ce4166a")
    cyUSDC = MintableForkToken("0x76eb2fe28b36b3ee97f3adae0c69606eedb2a37c")
    busdyDAI = MintableForkToken("0xC2cB1040220768554cf699b0d863A3cd4324ce32")
    busdyUSDC = MintableForkToken("0x26EA744E5B887E5205727f55dFBE8685e3b21951")
    busdyUSDT = MintableForkToken("0xE6354ed5bC4b393a5Aad09f21c46E101e692d447")
    yBUSD = MintableForkToken("0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE")
    yDAI = MintableForkToken("0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01")
    yUSDC = MintableForkToken("0xd6aD7a6750A7593E092a9B218d66C0A814a3436e")
    yUSDT = MintableForkToken("0x83f798e925BcD4017Eb265844FDDAbb448f1707D")
    yTUSD = MintableForkToken("0x73a052500105205d34Daf004eAb301916DA8190f")
    ycDAI = MintableForkToken("0x99d1Fa417f94dcD62BfE781a1213c092a47041Bc")
    ycUSDC = MintableForkToken("0x9777d7E2b60bB01759D0E2f8be2095df444cb07E")
    ycUSDT = MintableForkToken("0x1bE5d71F2dA660BFdee8012dDc58D024448A0A59")
    aDAI = MintableForkToken("0x028171bCA77440897B824Ca71D1c56caC55b68A3")
    aUSDC = MintableForkToken("0xBcca60bB61934080951369a648Fb03DF4F96263C")
    aUSDT = MintableForkToken("0x3Ed3B47Dd13EC9a98b44e6204A523E766B225811")
    aSUSD = MintableForkToken("0x6c5024cd4f8a59110119c56f8933403a539555eb")

    # Meta
    _3Crv = MintableForkToken("0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490")
    crvRenWSBTC = MintableForkToken("0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3")

    # ------------------------------------------------------------------------------

    CRV._mint_for_testing(ADDRESS, 100000 * 10 ** 18)
    # CVX._mint_for_testing(ADDRESS, 100000 * 10 ** 18)
    # DAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # USDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # USDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # sUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # renBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # WBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # sBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # HBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # GUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 2)
    # HUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 8)
    # USDK._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # USDN._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # LINKUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # mUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # RSV._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # TBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # DUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # pBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # BBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 8)
    # oBTC._mint_for_testing(ADDRESS, BTC_AMOUNT * 10 ** 18)
    # sETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    #
    # # EURS._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 2)
    # mint_by_swap(ADDRESS, EURS.address, sEUR.address, 18, "0x0Ce6a5fF5217e38315f87032CF90686C96627CAA", 1, 0, EUR_AMOUNT)
    #
    # sEUR._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 18)
    # EURT._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 6)
    # UST._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # stETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    # aETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    # USDP._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # LINK._mint_for_testing(ADDRESS, LINK_AMOUNT * 10 ** 18)
    # sLINK._mint_for_testing(ADDRESS, LINK_AMOUNT * 10 ** 18)
    # PAX._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # rETH._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # TUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # FRAX._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # LUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # BUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # alUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # MIM._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # WETH._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 18)
    # XAUt._mint_for_testing(ADDRESS, ETH_AMOUNT * 10 ** 6)
    # SPELL._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # T._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # RAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # EUROC._mint_for_testing(ADDRESS, EUR_AMOUNT * 10 ** 6)

    # WormholeUST._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # mint_by_swap(ADDRESS, WormholeUST.address, USDC.address, 6, "0x4e0915C88bC70750D68C481540F081fEFaF22273", 0, 2, USD_AMOUNT)

    # # Wrapped
    # cDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 8)
    # cUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 8)
    # cyDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 8)
    # cyUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 8)
    # cyUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 8)
    # busdyDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # busdyUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # busdyUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # yBUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # yDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # yUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # yUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # yTUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # ycDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # ycUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # ycUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # aDAI._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    # aUSDC._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # aUSDT._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 6)
    # aSUSD._mint_for_testing(ADDRESS, USD_AMOUNT * 10 ** 18)
    #
    # # Meta
    # _3Crv._mint_for_testing(ADDRESS, 100000 * 10 ** 18)
    # crvRenWSBTC._mint_for_testing(ADDRESS, 1000 * 10 ** 18)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
