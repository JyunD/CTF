#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *

context.arch = 'i386'

a = '''0x8     0x7b    0xba    0xff    0x2     0x5d    0x2f    0x66
0x47    0xe2    0x2e    0x2     0x53    0xd5    0x50    0x6e
0x4e    0xc     0x99    0xd6    0x4     0x32    0xef    0xb4
0x15    0xd2    0x40    0x39    0xe0    0x82    0x46    0xb3
0xaa    0xb7    0x2c    0xff    0x0     0x0     0x0     0x0
0x0     0x0     0x0     0x0     0x0     0x0     0x0     0x0
0x30    0xdc    0xff    0xf7    0x0     0x0     0x0     0x0
0x0     0x0     0x0     0x0     0x0     0x0     0x0     0x0
0x0     0x0     0x0     0x0     0x0     0xd0    0xff    0xf7
0x0     0x0     0x0     0x0     0x0     0x0     0x0     0x0
0x0     0x0     0x0     0x0     0x0     0x0     0x0     0x0
0x0     0x0     0x0     0x0     0x0     0x0     0x0     0x0
0x9     0x0     0x0     0x0     0x0     0xf0    0xfb    0xf7
0xc2    0x0     0x0     0x0     0xdb    0xd4    0xff    0xff
0x0     0xd0    0xff    0xf7    0xa0    0x41    0xfd    0xf7
0xa9    0x5     0xe8    0xf7    0xc2    0x0     0x0     0x0
0x84    0xc9    0xff    0xf7    0x88    0xc9    0xff    0xf7
0xda    0xd4    0xff    0xff    0x38    0x9     0xe8    0xf7
0xda    0xd4    0xff    0xff    0x84    0xc9    0xff    0xf7
0x88    0xc9    0xff    0xf7    0xe8    0xd4    0xff    0xff
'''
def step_one(input):
    first = [ i for i in range(256)]
    tmp = 0
    for index in range(256):
        v2 = first[index] + tmp
        tmp = (v2 + ord(input[index%11]) + 87) & 0xFF
        first[index], first[tmp] = first[tmp], first[index]
    return first

def step_two(first, origin):
    second = first.copy()
    dest = origin.copy()
    tmp = 0
    for index in range(160):
        tmp = (tmp + second[index+1]) & 0xFF
        second[index+1], second[tmp] = second[tmp], second[index+1]
        dest[index] ^= second[(second[index+1]+second[tmp]) & 0xFF]
    return dest

def shellcode(dest):
    tmp = ""
    for d in dest:
        tmp += hex(d)[2:].zfill(2)
    return bytes.fromhex(tmp)

origin = []
for c in a.split('\n'):
    origin += c.split()
    
origin = list(map(lambda x: int(x, 16),origin))

for key in range(100000000000):
    key = str(key).zfill(11)
    first = step_one(key)
    dest = step_two(first, origin)

    if dest[1] == 0xc3 and (dest[0] == 0x58 or dest[0] == 0x5b or dest[0] == 0x59 or dest[0] == 0x5a or dest[0] == 0x5e or dest[0] == 0x5f or dest[0] == 0x5d):
        print("key = {0}".format(key))
        break
