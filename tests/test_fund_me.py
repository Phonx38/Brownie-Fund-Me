from brownie import FundMe, network, accounts, exceptions
import pytest
from scripts.deploy import deploy_fundme
from scripts.helpful_scripts import getAccount, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_fund_and_withdraw():
    account = getAccount()
    fund_me = deploy_fundme()
    entrance_fee = fund_me.getEntranceFee()
    tx1 = fund_me.fund({"from": account, "value": entrance_fee})
    tx1.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = getAccount()
    fund_me = deploy_fundme()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
