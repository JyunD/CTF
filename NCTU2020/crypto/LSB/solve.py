#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pwn import *
from Crypto.Util.number import *

p = remote('140.112.31.97', '30001')

p.recvuntil("n = ")
n = int(p.recvline())

p.recvuntil("c = ")
c = int(p.recvline())

e = 65537

top = n
bottom = 0

coff = pow(3, e, n)

while True:
    c = (coff * c) % n
    
    p.sendline(str(c))

    bit = int(p.recvline()[-2])

    tmp = top - bottom

    if bit == 0:
        top = bottom + tmp // 3 + 1
    elif bit == (-n % 3):
        top = bottom + 2 * tmp // 3 + 1
        bottom = bottom + tmp // 3
    else:
        bottom = bottom + 2 * tmp // 3

    if top - bottom <= 2:
        break

info(bottom)
success(long_to_bytes(bottom))

p.interactive()
p.close()