#!/usr/bin/env python3
import time
import random
from typing import List

def trans(data, size=4):
    return [int.from_bytes(data[index:index+size], 'big') for index in range(0, len(data), size)]

def reverse_trans(data, size=4):
    return b''.join([element.to_bytes(size, 'big') for element in data])

def _encrypt(vector: List[int], key: List[int]):
    sum, delta, mask = 0, 0xFACEB00C, 0xffffffff
    for _ in range(32):
        sum = sum + delta & mask
        vector[0] = vector[0] + ((vector[1] << 4) + key[0] & mask ^ (vector[1] + sum) & mask ^ (vector[1] >> 5) + key[1] & mask) & mask
        vector[1] = vector[1] + ((vector[0] << 4) + key[2] & mask ^ (vector[0] + sum) & mask ^ (vector[0] >> 5) + key[3] & mask) & mask
    return vector

def encrypt(plaintext: bytes, key: bytes):
    cipher = b''
    for index in range(0, len(plaintext), 8):
        cipher += reverse_trans(_encrypt(trans(plaintext[index:index+8]), trans(key)))
    return cipher

if __name__ == '__main__':
    flag = open('flag', 'rb').read()
    assert len(flag) == 16
    random.seed(int(time.time()))
    key = random.getrandbits(128).to_bytes(16, 'big')
    cipher = encrypt(flag, key)
    print(f'cipher = {cipher.hex()}')
