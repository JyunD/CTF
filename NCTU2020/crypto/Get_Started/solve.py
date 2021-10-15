#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from address import *
import json
from web3 import Web3
from solc import compile_standard
import time
from pwn import  *

GetStarted_sol = open('./GetStarted.sol').read()
p = remote('140.112.31.97', '30002')


def Start():
    global w3, compiled_sol, FACTORY_ADDRESS, token, FACTORY_ABI, FACTORY_BYTECODE, GETSTART_ABI, GETSTART_BYTECODE

    p.recvuntil('>')
    p.sendline("1")
    p.recvuntil('Factory Contract Address : ')
    FACTORY_ADDRESS = p.recvline()[:-1]
    p.recvuntil('call validate(')
    token = p.recv(66)
    p.recvuntil("----- flag will appear below -----")

    w3 = Web3(Web3.WebsocketProvider('wss://ropsten.infura.io/ws/v3/faa6cd8da8984cc7b95b935d1bede5c7'))
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources":
        {
            "GetStarted.sol": {
                "content": GetStarted_sol
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
    FACTORY_ABI = json.loads(compiled_sol['contracts']['GetStarted.sol']['GetStartedFactory']['metadata'])['output']['abi']
    FACTORY_BYTECODE = compiled_sol['contracts']['GetStarted.sol']['GetStartedFactory']['evm']['bytecode']['object']

    GETSTART_ABI = json.loads(compiled_sol['contracts']['GetStarted.sol']['GetStarted']['metadata'])['output']['abi']
    GETSTART_BYTECODE = compiled_sol['contracts']['GetStarted.sol']['GetStarted']['evm']['bytecode']['object']


if __name__ == "__main__":
    
    Start()
    factory = Contract(FACTORY_ABI, FACTORY_BYTECODE, FACTORY_ADDRESS.decode('ascii'))

    factory.send_transaction('create', address, private_key)
    
    addr = factory.call('instances', address)
    
    getstarted = Contract(GETSTART_ABI, GETSTART_BYTECODE, addr)

    getstarted.send_transaction('callme', address, private_key)

    factory.send_transaction('validate', address, private_key, int(token, 16))

    print("END")

    while True:
        print(p.recvline())
        time.sleep(1)