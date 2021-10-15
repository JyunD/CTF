#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *

p = remote('eofqual.zoolab.org', '10110')

p.recvuntil("聊天室房間號碼: ")
passwd = p.recv(96)

iv = passwd[:16]
cipher = passwd[16:-32]
md5 = passwd[-32:]

p.recvuntil("系統訊息: 加密連線完成，開始聊天囉！")

print("start")


def xor(a, b):
    length = len(b)
    return hex(int(a, 16) ^ int(b, 16))[2:].zfill(length).encode('ascii')


def check_head(index, iv, cipher):
    for i in range(1<<7):
        for j in range(1<<1):
            for k in range(1<<1):
                p.recvuntil("輸入訊息: ")
                
                head = []
                res = b""

                head.append(hex(int('1' + f"{i:07b}", 2))[2:].zfill(2))
                head.append(hex(int('1' + f"{j:01b}" +'0'*6, 2))[2:].zfill(2))
                head.append(hex(int('1' + f"{k:01b}" +'0'*6, 2))[2:].zfill(2))

                for h in range(len(head)):
                    res += xor(head[h], iv[index*2+h*2:index*2+h*2+2].decode('utf-8'))
                res = iv[:index*2] + res + iv[(index+3)*2:] + cipher

                p.sendline(res)
                output = p.recvline()
                if "陌生人" in output.decode('utf-8'):
                    return head

def check_body(index, head, iv, cipher):
    for i in range(1<<4):
        for j in range(1<<6):
            for k in range(1<<6):
                p.recvuntil("輸入訊息: ")
                
                body = []
                res = b""
            
                body.append(hex(int(f"{int(head[0], 16):08b}"[:4] + f"{i:04b}", 2))[2:].zfill(2))
                body.append(hex(int(f"{int(head[1], 16):08b}"[:2] + f"{j:06b}", 2))[2:].zfill(2))
                body.append(hex(int(f"{int(head[2], 16):08b}"[:2] + f"{k:06b}", 2))[2:].zfill(2))
                
                for h in range(len(body)):
                    res += xor(body[h], iv[index*2+h*2:index*2+h*2+2].decode('utf-8'))
                body = res
                res = iv[:index*2] + res + iv[(index+3)*2:] + cipher

                p.sendline(res)
                output = p.recvline()

                if "對方離開了" in output.decode('utf-8'):
                    return body

def per_block(iv, cipher):
    F = ""
    for index in range(0, 6, 3):

        head = check_head(index, iv, cipher)
        body = check_body(index, head, iv, cipher)
        tmp = xor(xor(body, "e794b7").decode('ascii'), iv[(index*2):(index*2)+6]).decode('ascii')
        F += bytes.fromhex(tmp).decode('utf-8')

    index = 5
    
    F = F[:-1]

    head = check_head(index, iv, cipher)
    body = check_body(index, head, iv, cipher)
    tmp = xor(xor(body, "e794b7").decode('ascii'), iv[(index*2):(index*2)+6]).decode('ascii')

    F += bytes.fromhex(tmp).decode('utf-8')

    return F

flag = ""
F = per_block(iv, cipher[:16])
print(flag)
flag += F
F = per_block(cipher[:16], cipher[16:32])
print(flag)
flag += F
F = per_block(cipher[16:32], cipher[32:])
print(flag)
flag += F


print(flag)


p.interactive()
p.close()