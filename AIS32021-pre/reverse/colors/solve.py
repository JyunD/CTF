#!/usr/bin/python3
# -*- coding: UTF-8 -*-

encoded = "BgiJ6\w1Aj\\1guikl7xiXKIhXKil6fo65Kn87B-8warzK"
key = "AlS3{BasE64_i5+b0rNIng~\Qwo/-xH8WzCj7vFD2eyVktqOL1GhKYufmZdJpX9}"

low = []
mid = list(map(int,list("423560343444373134655114504577415715745143147")))
high = list(map(int,list("000101000101000000000000001100000011010101010")))

flag = ""


for e in encoded:
    low.append(key.index(e))

for i in range(0, len(encoded)//4):
    tmp = ""
    for j in range(4):
        h = high[4*i + j]
        m = mid[4*i + j]
        l = low[4*i + j]
        tmp += f"{h:01b}" + f"{m:03b}" + f"{l:06b}"

    for j in range(0,40,8):
        flag += chr(int(tmp[j:j+8], 2))


print(flag)
# AIS3{base1024_15_c0l0RFuL_GAM3_CL3Ar_thIS_IS_y0Ur_FlaG!}