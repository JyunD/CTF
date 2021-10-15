#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from Crypto.Util.number import *
import string
import owiener
import hashlib

def change(cipher):
    tmp = ""
    for c in cipher:
        if c in string.ascii_uppercase:
            tmp += chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
        elif c in string.ascii_lowercase:
            tmp += chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
        else:
            tmp += c
    return tmp

ciphers = []
signs = []

for folder in range(1,11):
    f = str(folder).zfill(2)

    with open(f+"/Ciphertext.txt", "r") as file:
        ciphers.append(int(file.read(), 16))

    with open(f+"/Signature.txt", "r") as file:
        signs.append(int(file.read(), 16))


# Public_KeyA
n = int("00CEFFB3C3F9ACA67C993B07333A37FD442418E4DB9E71597AF4DED238F14A96B61C82EDCFFAF06F7A8ABA7D74F8F2B55E2760907E6E810E3DF664EF68EC8B69B9", 16)
e = int("0084747AC35C706DD82CF4E8968F1A64A5C5B3683E601487FD75D35F11B0D4D9BA67A54616093DA17FABBD2E9E49A64F2967A7F2899E007AE2F313C27CFE353101", 16)

d = owiener.attack(e, n)

plaintexts = [(long_to_bytes(pow(cipher, d, n))).decode('utf-8') for cipher in ciphers]


# Public_KeyB
n = int("00A67593E840E5EDF67D82F0C5D97279B479ABD84588FCD3C9F6BAD94994FA3EB9CE3FF9AEB6ADFCB0AA9BFC0F90CDE853DE253DA3CE998ADFE72F735E1E8FB4BF", 16)
e = int("10011", 16)

for plaintext,sign in zip(plaintexts,signs):
    m = hashlib.md5()
    m.update(plaintext.encode('utf-8'))
    md5 = int(m.hexdigest(), 16)
    if md5 == pow(sign, e, n):
        print(change(plaintext))