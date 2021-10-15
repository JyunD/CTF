#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from web3 import Web3


if __name__ == "__main__":

    w3 = Web3(Web3.WebsocketProvider('wss://ropsten.infura.io/ws/v3/faa6cd8da8984cc7b95b935d1bede5c7'))
    flag = w3.eth.getStorageAt('0x21546F53AC81DDfc2b618D5617d173e43661366c', 0)

    print(str(flag))