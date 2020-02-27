#!/usr/bin/python
# -*- coding: utf-8 -*-

from pwn import *

p = remote('final.ctf.bitx.tw', '30003')

p.recvuntil('There are 500 questions, good luck!\n\n')

for i in range(500):

    formula = p.recvuntil('=')[:-1]

    p.sendlineafter('Answer =', str(eval(formula)))


p.interactive()