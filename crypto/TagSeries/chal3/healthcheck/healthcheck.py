#!/usr/bin/env python3
from struct import pack
from pwn import remote, process
import sys

DEBUG = False


class custom_sha1:
    def __init__(self):
        self._buffer = bytearray()

    def update(self, data: bytes):
        if not isinstance(data, (bytearray, bytes)):
            raise TypeError(f"expected bytes for data, got {type(data)}")

        self._buffer.extend(data)
        return self

    def hexdigest(self, extra_length=0, initial_state=None):
        tag = sha1(
            bytes(self._buffer),
            extra_length=extra_length,
            initial_state=initial_state)
        self._buffer = bytearray()
        return tag


def sha1(
        message: bytes,
        initial_state=None,
        extra_length=0   # in BYTES
    ) -> str:
    H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    if initial_state is not None:
        if len(initial_state) != 5 or \
            any(not isinstance(x, int) for x in initial_state):
            raise TypeError(f"expected list of 5 ints, got {initial_state}")
        H = initial_state

    # pad according to the RFC (and then some, if specified)
    pad = create_padding(message, extra_length)
    padded_msg = message + pad

    # break message into chunks
    M = [padded_msg[i:i+64] for i in range(0, len(padded_msg), 64)]
    assert len(M) == len(padded_msg) / 64
    for i in range(len(M)):
        assert len(M[i]) == 64  # sanity check

    # do hashing voodoo
    for i in range(len(M)):
        W = [
            int.from_bytes(M[i][j:j+4], byteorder="big")
            for j in range(0, len(M[i]), 4)
        ]
        assert len(W) == 16
        assert type(W[0]) == int
        assert W[0] == (M[i][0] << 24) + (M[i][1] << 16) + (M[i][2] << 8) + M[i][3]

        for t in range(16, 80):
            W.append(_S(1, W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16]))

        A, B, C, D, E = H
        for t in range(80):
            TEMP = (((((((_S(5, A) + _f(t, B, C, D)) & 0xFFFFFFFF) + E) & 0xFFFFFFFF) + W[t]) & 0xFFFFFFFF) + _K(t)) & 0xFFFFFFFF
            assert TEMP == (_S(5, A) + _f(t, B, C, D) + E + W[t] + _K(t)) & 0xFFFFFFFF
            E, D, C, B, A = D, C, _S(30, B), A, TEMP

        H = [
            (H[0] + A) & 0xFFFFFFFF,
            (H[1] + B) & 0xFFFFFFFF,
            (H[2] + C) & 0xFFFFFFFF,
            (H[3] + D) & 0xFFFFFFFF,
            (H[4] + E) & 0xFFFFFFFF,
        ]

    # craft the hex digest
    th = lambda h: hex(h)[2:] # trimmed hex
    return "".join("0" * (8 - len(th(h))) + th(h) for h in H)


def _f(t, B, C, D):
    if t >= 0 and t <= 19:    return ((B & C) | ((~B) & D)) & 0xFFFFFFFF
    elif t >= 20 and t <= 39: return (B ^ C ^ D) & 0xFFFFFFFF
    elif t >= 40 and t <= 59: return ((B & C) | (B & D) | (C & D)) & 0xFFFFFFFF
    elif t >= 60 and t <= 79: return (B ^ C ^ D) & 0xFFFFFFFF
    assert False


def _K(t):
    if t >= 0 and t <= 19:    return 0x5A827999
    elif t >= 20 and t <= 39: return 0x6ED9EBA1
    elif t >= 40 and t <= 59: return 0x8F1BBCDC
    elif t >= 60 and t <= 79: return 0xCA62C1D6
    assert False

def _S(n, X):
    assert n >= 0 and n < 32, "n not in range"
    assert (X >> 32) == 0, "X too large"
    result = ((X << n) | (X >> (32-n))) & 0xFFFFFFFF
    assert (result >> 32) == 0, "result too large"
    return result


def create_padding(
        message: bytes,
        extra_length: int = 0   # in BYTES
    ) -> bytes:
        l = (len(message) + extra_length) * 8
        l2 = ((l // 512) + 1) * 512
        padding_length = l2 - l
        if padding_length < 72:
            padding_length += 512
        assert padding_length >= 72, "padding too short"
        assert padding_length % 8 == 0, "padding not multiple of 8"

        # Encode the length and add it to the end of the message.
        zero_bytes = (padding_length - 72) // 8
        length = pack(">Q", l)
        pad = bytes([0x80] + [0] * zero_bytes)

        return pad + length


def length_extend(message: bytes, injection: bytes, extra_length: int, tag: bytes):
    hasher = custom_sha1()

    state = [int(tag[i:i+8], 16) for i in range(0, len(tag), 8)]

    hasher.update(injection)

    new_tag = hasher.hexdigest(initial_state=state, extra_length=len(b'1' * extra_length + message + create_padding(b'1' * extra_length + message)))

    message = message + create_padding(message, extra_length=extra_length) + injection

    return message, new_tag


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
    initial_hash = r.recvline().strip()
    print(f"Initial hash: {initial_hash}")
    new_message, new_hash = length_extend(b"GET FILE: ", b"flag.txt", 1200, initial_hash)
    r.sendline(new_message)
    r.sendline(new_hash.encode())
    print(r.recvall().decode().strip())


if __name__ == "__main__":
    main()
