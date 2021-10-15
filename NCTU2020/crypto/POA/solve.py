#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pwn import *
import binascii

p = remote('140.112.31.97', '30000')

p.recvuntil("cipher = ")

cipher = p.recvline()[:-1]

info(cipher)

def check_padding(cipher, index):

    tmp = []
    for i in range(256):

        payload = cipher[:index] + hex(i)[2:].zfill(2) + cipher[index+2:]

        p.sendlineafter('cipher = ', payload)
        string = p.recv(10)

        if string == "YESSSSSSSS":
            tmp.append(i)

    return tmp


def per_block(start, cipher, index, plaintext):

    if index < start:
        return plaintext

    info(str(index))

    tmp = check_padding(cipher, index)

    if 0 < len(tmp) <= 2:
        for branch in tmp:
            new = cipher[:index] + hex(branch ^ 128)[2:].zfill(2) + cipher[index+2:]
            new_plaintext = hex(int(cipher[index:index+2], 16) ^ branch ^ 128)[2:].zfill(2) + plaintext

            end = per_block(start, new, index-2, new_plaintext)

            if end != None:
                return end


plaintext = ""

length = len(cipher) - 32
for byte in range(length, 0, -32):

    plaintext = per_block(byte-32, cipher, byte-2, plaintext)
    cipher = cipher[:-32]

success(binascii.unhexlify(plaintext))

p.interactive()
p.close()

# FLAG{31a7f10f1317f622}