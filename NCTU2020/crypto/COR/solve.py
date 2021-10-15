#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from functools import reduce
from itertools import product

output = [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1]

class LFSR:
    def __init__(self, init, feedback):
        self.state = init
        self.feedback = feedback
    def getbit(self):
        nextbit = reduce(lambda x, y: x ^ y, [i & j for i, j in zip(self.state, self.feedback)])
        self.state = self.state[1:] + [nextbit]
        return nextbit


def check_same(x, y):
    return float(list(map(lambda x,y : x^y, x, y)).count(0))/(len(x))


A = []
B = []
C = []

for bit in range(2**16):

    init = [int(i) for i in f"{int.from_bytes(bytes([bit//256, bit%256]), 'big'):016b}"]
    b = LFSR(init, [int(i) for i in f'{40111:016b}'])
    b_output = [b.getbit() for _ in range(100)]
    if check_same(b_output, output) >= 0.75:
        B.append((init, b_output))
    del b

for bit in range(2**16):

    init = [int(i) for i in f"{int.from_bytes(bytes([bit//256, bit%256]), 'big'):016b}"]
    c = LFSR(init, [int(i) for i in f'{52453:016b}'])
    c_output = [c.getbit() for _ in range(100)]
    if check_same(c_output, output) >= 0.75:
        C.append((init, c_output))
    del c

for bit in range(2**16):

    init = [int(i) for i in f"{int.from_bytes(bytes([bit//256, bit%256]), 'big'):016b}"]
    a = LFSR(init, [int(i) for i in f'{39989:016b}'])
    a_output = [a.getbit() for _ in range(100)]

    for x, y in product(B, C):
        for i in range(100):
            if output[i] != (a_output[i] & x[1][i]) ^ ((not a_output[i]) & y[1][i]):
                del a
                break

        if i == 99:
            A = init
            B = x[0]
            C = y[0]
            break
    if i == 99:
        break

string = [A, B, C]


FLAG = b"FLAG{"

for s in string:
    tmp = int(''.join([str(i) for i in s]), 2)
    FLAG += bytes([tmp//256, tmp%256])

FLAG += b'}'

print(FLAG)
