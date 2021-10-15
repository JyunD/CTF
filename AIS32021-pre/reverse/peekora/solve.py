#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from itertools import product
import string
from pwn import *

flag_head = "AIS3{dAmwjzphI"
a = ""

for c in string.printable[:-5]:
    
    p = process("python3 -m pickle flag_checker.pkl".split())

    p.recvuntil("FLAG: ")

    flag = flag_head + c+ "}"

    p.sendline(flag)

    try:
        a = p.recvline()[:-1]
        p.recvline()
        if (a == b"Correct!"):
            break
    except:
        print("error")
    
    p.close()

print(flag)

p.interactive()
# AIS3{dAmwjzphIj}