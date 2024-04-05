#!/usr/bin/env python3
from pwn import remote, process
import sys

DEBUG = False


def main():
    if DEBUG:
        r = process(["python3", "challenge/chal.py"])
    else:
        addr = "127.0.0.1"
        port = 1337
        if len(sys.argv) > 1:
            addr = sys.argv[1]
        if len(sys.argv) > 2:
            port = sys.argv[2]
        r = remote(addr, port)

    r.recvuntil(b"== proof-of-work: ")
    if r.recvline().startswith(b"enabled"):
        print(r.recvuntil(b"python3 "))
        print(r.recvuntil(b" solve "))
        challenge = r.recvline().decode("ascii").strip()
        p = process(["kctf_bypass_pow", challenge])
        solution = p.readall().strip()
        r.sendline(solution)
        print(r.recvuntil(b"Correct\n"))

    # Receive the initial hash
    msg1 = b"aaaaaaaaaaaaaaaa"
    msg2 = b"GET: flag.txt\0\0\0"
    msg3 = b"flag.txt\0\0\0\0\0\0\0\0"
    r.sendline(msg1)
    r.sendline(b"a")
    c1 = r.recvline().strip()
    r.sendline(msg2)
    r.sendline(b"a")
    c2 = r.recvline().strip()
    r.sendline(msg1 + len(msg1).to_bytes(16, "big") + bytes(a ^ b for a, b in zip(msg3, c1)))
    r.sendline(b"a")
    c3 = r.recvline().strip()
    r.sendline(msg2 + len(msg2).to_bytes(16, "big") + bytes(a ^ b for a, b in zip(msg3, c2)))
    r.sendline(c3)
    ans = r.recvall().decode().strip()
    print(ans)
    if ans.startswith("wctf{"):
        exit(0)
    else:
        main()


if __name__ == "__main__":
    main()
