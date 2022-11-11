#!/usr/bin/python3

from brownie import config, accounts, Contract, interface

config['autofetch_sources'] = True


ADDRESS = accounts[0].address


class _MintableTestToken(Contract):

    def __init__(self, address, interface_name):
        abi = getattr(interface, interface_name).abi
        self.from_abi(interface_name, address, abi)

        super().__init__(address)

    def _mint_for_testing(self, target, amount, kwargs=None):
        if self.address == "0x90Ca507a5D4458a4C6C6249d186b6dCb02a5BCCd":  # DAI
            self.transfer(target, amount, {"from": "0xccd9d850ef40f19566cd8df950765e9a1a0b9ef2"})
        if self.address == "0xef4229c8c3250C675F21BCefa42f58EfbfF6002a":  # USDC
            self.transfer(target, amount, {"from": "0x9aa92a827Baa2D47a225614e4e5375AF10f78a29"})
        if self.address == "0x88eeC49252c8cbc039DCdB394c0c2BA2f1637EA0":  # USDT
            self.transfer(target, amount, {"from": "0xC77398cfb7B0F7ab42baFC02ABc20A69CE8cEf7f"})

def main():
    DAI = _MintableTestToken("0x90Ca507a5D4458a4C6C6249d186b6dCb02a5BCCd", "ERC20")
    USDC = _MintableTestToken("0xef4229c8c3250C675F21BCefa42f58EfbfF6002a", "ERC20")
    USDT = _MintableTestToken("0x88eeC49252c8cbc039DCdB394c0c2BA2f1637EA0", "ERC20")

    # ------------------------------------------------------------------------------

    DAI._mint_for_testing(ADDRESS, 10000 * 10 ** 18)
    USDC._mint_for_testing(ADDRESS, 10000 * 10 ** 6)
    USDT._mint_for_testing(ADDRESS, 10000 * 10 ** 6)

    if ADDRESS != accounts[0].address:
        accounts[0].transfer(ADDRESS, "100 ether")
