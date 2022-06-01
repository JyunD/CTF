#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from Crypto.Util.number import long_to_bytes
from pwn import *

context.arch = 'amd64'
p = remote('crypto.heroctf.fr', 9000)

cipher = int(p.recvline()[2:-1])

p.sendlineafter(b'c=', str(-1).encode())
n = int((int(p.recvline()[:-1]) + 1))

p.sendlineafter(b'c=', str(2).encode())
c_2 = int((int(p.recvline()[:-1])))

for i in range(3, 65537):

    m_2 = pow(c_2, i, n)
    if m_2 == 2:
        e = i
        break


p.sendlineafter(b'c=', str(pow(2, e, n)*cipher%n).encode())
m = int((int(p.recvline()[:-1])))

print(long_to_bytes(m//2))