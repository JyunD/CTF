#!/usr/bin/python3
# -*- coding: utf-8 -*-

import hashlib
from string import printable

func = (lambda s: (int(__import__('hashlib').sha224(s).hexdigest(), 16) ^ int(__import__('hashlib').sha256(s).hexdigest(), 16) ^ int(__import__('hashlib').sha384(s).hexdigest(), 16) ^ int(__import__('hashlib').sha512(s).hexdigest(), 16)) & 0xFFFFFFFF)

cipher = '''376458635
2233597867
354029087
1915420169
3254692394
2815960165
4110859573
3306584243
1848860968'''

cipher = [int(i) for i in cipher.split()]
flag = ""

for i in cipher:
    f = False
    for j in printable:
        for k in printable:
            tmp = j + k
            if func(str.encode(tmp)) == i:
                flag += tmp
                f = True
            if f:
                break

        if f:
            f = False
            break
print(flag)