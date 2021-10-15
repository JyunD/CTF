#!/usr/bin/env python3
import random
from Crypto.Util.number import *

FLAG = b"FLAG{nF9Px2LtlNh5fJiq3QtG}"


def pad(data, block_size):
    padlen = block_size - len(data) - 2
    if padlen < 8:
        raise ValueError
    return b'\x00' + bytes([random.randint(1, 255) for _ in range(padlen)]) + b'\x00' + data

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
d = inverse(e, (p - 1) * (q - 1))

m = bytes_to_long(pad(FLAG, 128))
c = pow(m, e, n)
print(f'm = {m}')
print(f'n = {n}')
print(f'c = {c}')
print(f'd = {d}')
