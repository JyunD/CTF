#!/usr/bin/python3
# -*- coding: utf8 -*-

def trans_caesar(input, offset):

    output = ''.join([chr(ord(i) + offset) for i in input])

    return output

cipher = "MNDq9W)i*HUbiUD&jU&d_oU(,s"

plaintext = trans_caesar(cipher, (ord('W') - ord(cipher[0])))

print(plaintext)