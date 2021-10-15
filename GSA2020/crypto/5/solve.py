#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
from Crypto.Util.number import *

cipher = int("9646670132b586e5a8a52d619f399827a3dc83895c8cb1c1e1bc99ed3c4a5f9dff35854a07226877aef1ad68d270670121a6436a1980e9d3e1f3d768244c501ccc13e8777fffc6a921d0113cb83fac8cc12fdd07011346e8d3e2d55788d0597f7ff05530e486d42987583625bdd0d08176bbe1c3e8a46b2c7aa643dedc1d65e5", 16)

p = 13366167429494305372769128434146013096716923404270450732746859751847798864498643931204952238822168793212213491754853450191926519963687655238493197725915859

q = 11692246070975972376144070223291675179761535406487055848965141482300924068035666475043383048259063864464324839393511057038260578921212111612486060040875597

N = p * q
e =  int('10001', 16)

d = inverse(e, (p-1)*(q-1))


IV = hex(pow(cipher, d, N))

print(IV)

key = hex(13366167429494305372769128434146013096716923404270450732746859751847798864498715363746262672464293691271513287874353731827564093663378662434744120871727791 ^ 13366167429494305372769128434146013096716923404270450732746859751847798864498643931204952238822168793212213491754853450191926519963687655238493197725915859)

aes = AES.new(mode=AES.MODE_CBC, key=(key[2:]).encode('utf-8'), iv=(IV[2:]).encode('utf-8'))
# aes.encrypt