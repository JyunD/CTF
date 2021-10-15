#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *
from binascii import hexlify

r = remote('quiz.ais3.org', '42069')

r.sendlineafter("3) exit\n", "1")
r.sendlineafter("Name (in hex): ", b"00" + hexlify(b'Ethan Winters'))

sig = r.recvline()[11:-1]

r.sendlineafter("3) exit\n", "2")
r.sendlineafter("Signature: ", sig)


r.interactive()
# AIS3{R3M383R_70_HAsh_7h3_M3Ssa93_83F0r3_S19N1N9}