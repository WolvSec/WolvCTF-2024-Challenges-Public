
start = 0x3148

seq = []
for _ in range(24):
    seq.append(start % 256)
    if start % 2 == 0:
        start //= 2
    else:
        start *= 3
        start += 1
        start %= 0x10000
print(seq)

key = open('../challenge/prog', 'rb').read()[0x10f1:0x11f1]
xorkey = [key[i] for i in seq]
print(xorkey)
flag = b'wctf{h4ppy_d3c0mp1l1ng!}'

assert len(flag) == len(xorkey)

data = [f'{flag[i] ^ xorkey[i]:02x}' for i in range(len(flag))]
print('\n'.join(f'db 0x{x}' for x in data))

