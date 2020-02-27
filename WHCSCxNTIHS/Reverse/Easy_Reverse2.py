#!/usr/bin/python3
# -*- coding: utf8 -*-

import time
import random
from string import printable

cipher = '''0110011101111010
1100100011011110
0110011110010101
1000011111100110
1101010111011010
1100110100100001
0101011111100001
0101110111010100
1010001110000001
0100111110100101
0111000001001101
0100101010011101
0001000001110110
1100011100111100
1101000000011111
1101111011000101
0111001000000000
1111001110100101'''

cipher = cipher.split()

random.seed(1582119378)

def rand():
    rnd = int(random.random() * (10 ** 5))
    while rnd:
        random.random()
        rnd -= 1
    return int(random.random() * 10 ** 5) & ((1 << 16) - 1)


def calc(ch, rnd):
    high = ch >> 4
    low = ch & 0xF

    _00 = (low << 4) | low
    _01 = (low << 4) | high
    _10 = (high << 4) | low
    _11 = (high << 4) | high

    val = 0
    val |= _00 << 12
    val |= _11 << 8
    val |= _01 << 4
    val |= _10 << 0

    res = 0
    res |= 0b0000111100001111 & (val ^ rnd)
    res |= 0b1111000011110000 & (val ^ rnd)
    res |= 0b0101010101010101 & (val ^ rnd)
    res |= 0b1010101010101010 & (val ^ rnd)

    return bin(res).lstrip('0b').zfill(16)


def all_different(val):
    lst = []
    for ch in printable:
        lst.append(calc(ord(ch), val))
    return len(lst) == len(set(lst))




flag = ""
for index, res in enumerate(cipher):
    _rand = rand()
    for ch in printable:
        if calc(ord(ch), _rand) == res:
            flag += ch


print(flag)
