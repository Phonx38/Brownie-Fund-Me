from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def getAccount():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_price_feed_address():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        return price_feed_address
    else:
        print(f"Active network is {network.show_active()}")
        print("Deploying Mocks")
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(
                DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": getAccount()}
            )
        print("Mocks Deployed")
        price_feed_address = MockV3Aggregator[-1].address
        return price_feed_address
