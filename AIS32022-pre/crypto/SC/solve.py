#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *

with open("./cipher.py", "r") as file:
    cipher = file.read()

with open("./cipher.py.enc", "r") as file:
    plaintext = file.read()

with open("./flag.txt.enc", "r") as file:
    flag_c = file.read()

key = dict()

for c, t in zip(cipher, plaintext):
    key[c] = t

flag = ""

for f in flag_c:
    flag += list(key.keys())[list(key.values()).index(f)]

print(flag)