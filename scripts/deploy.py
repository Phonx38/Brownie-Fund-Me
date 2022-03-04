from brownie import FundMe, config, network
from scripts.helpful_scripts import getAccount, get_price_feed_address


def deploy_fundme():
    account = getAccount()
    # pass the pricefeed address to fundme contract

    # if we are on persistent address like rinkeby use assocciatedaddress else deplou mocks
    fund_me = FundMe.deploy(
        get_price_feed_address(),  # priceFeed address
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fundme()
