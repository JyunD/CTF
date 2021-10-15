#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pwn import *

context.arch = 'amd64'

p = remote('the-last-bitcoin.balsnctf.com', '7123')

p.recvuntil("??? = ")

p.sendline("\x80")

p.interactive()
p.close()
