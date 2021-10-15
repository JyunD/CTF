#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from gmpy2 import gcdext

# ax + by = 1

y_list = [ int(i, 16) for i in ['C8F9A829','EC83260E','AF93C6F4','5A1B89D9','31E68D0D','C38CE7E7','C8F9A829','4AEE907B','E0138A5F','31E68D0D','09975E45','D129EA43','C6830A2F','C8F9A829','EC83260E','EC83260E','13BF2B7F','E0138A5F','E419B183','B2F1DDBB','C38CE7E7','C38CE7E7','91639414','5A1B89D9','31E68D0D','8C45C2B1','0C76C360','0876805B','8D67DD2C','C212D77C','EC83260E','5A1B89D9','E59D8403','77244701','1499761A','EB6552FE']]

index_list = [ int(i, 16) for i in ['0F','20','01','1D','17','12','0E','1F','1A','08','1B','02','10','14','15','22','13','1C','18','16','05','07','03','19','06','00','0D','0C','1E','0B','21','09','23','0A','11','04']]

a = int('0FBC56A93', 16)
flag = [0] * 36

for index in range(36):

    for char in range(32,127):
        gcd ,x ,y = gcdext(a, char)

        if y < 0:
            y = int(y) + a
        
        if y == y_list[index]:
            flag[index_list[index]] = char
            break

print(''.join(list(map(chr,list(map(int,flag))))))
# FLAG{gogo_p0werr4ng3r!you_did_IT!!!}