# Debug script with same functionality as shredded.c

flag = [b'w', b'c', b't', b'f',b'{', b's', b'H', b'r', b'3', b'D', b'D', b'i', b'n', b'G', b'_', b'L', b'1', b'k', b'3', b'_', b'H', b'3', b'N', b'D', b'r', b'1', b'x', b'_', b'9', b'3', b'2', b'8', b'4', b'}']

def swap(a, i1, i2):
    a[i1], a[i2] = a[i2], a[i1]

i = len(flag)
while len(flag) < 49:
    flag.append(flag[(len(flag)*2)%i])
flag.append(b'\0')

for i in range(50):
    swap(flag, i, ((i+7)*15)%50)

for i in range(50):
    swap(flag, i, ((i+3)*7)%50)

for i in range(50):
    swap(flag, i, ((i+83)*12)%50)

for i in range(50):
    flag[i] = int.from_bytes(flag[i]) ^ 0x20
    flag[i] = flag[i] ^ 0x5

print(flag)

for i in flag:
    print(hex(i), end=" ")