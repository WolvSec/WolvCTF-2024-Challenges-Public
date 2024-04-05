contents = open('flag.txt.enc', 'rb').read()

for group in [contents[i:i+4] for i in range(0, 48, 4)]:
    a = int.from_bytes(group, 'little')
    a = (a >> 13) | (a << 19)
    a %= 2**32
    print(a.to_bytes(4, 'little').decode(), end='')
