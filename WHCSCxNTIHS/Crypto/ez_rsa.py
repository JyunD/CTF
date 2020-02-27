#!/usr/bin/python3
# -*- coding: utf8 -*-

import binascii
def Extend_Euclidean(m, n):
    if m == 0:
        return 0 , 1 , n
    else:
        x , y , q = Extend_Euclidean( n%m , m)
        x , y =  (y-(n//m)*x) , x
        return x , y , q 


p = 217343273395108011208730630854047871183
q = 185739083403452700209974536095724600133

e = 13337


n = p * q
phi = (p - 1) * (q - 1)

d = Extend_Euclidean(e, phi)[0] % phi

cipher = 38701601533462127138915399931209000290344258442601301168697904838260946244394
decrypted = pow(cipher, d, n)


print(binascii.unhexlify(hex(int(decrypted))[2:]))