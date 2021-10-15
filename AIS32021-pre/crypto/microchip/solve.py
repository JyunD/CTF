#!/usr/bin/python3
# -*- coding: UTF-8 -*-
def shift(cipher, key):
    return chr((ord(cipher) - 32 - key) % 96 + 32)

cipher = "=Js&;*A`odZHi'>D=Js&#i-DYf>Uy'yuyfyu<)Gu"
ais3 = "AIS3"
flag = ""
key = []

for c , a in zip(cipher[0:4][::-1],ais3):
    key.append(int((ord(c) - ord(a)) % 96))

for i in range(0, len(cipher), 4):
    temp = cipher[i:i+4][::-1]
    for c , k in zip(temp, key):
        flag += shift(c, k)
        
print(flag)
# AIS3{w31c0me_t0_AIS3_cryptoO0O0o0Ooo0}