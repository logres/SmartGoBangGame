from brownie import Gobang, accounts, network
import dotenv
import os



def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(os.getenv("PRIVATE_KEY1"))

def main():
    account1 = get_account()

    game = Gobang.deploy({"from": account1})
