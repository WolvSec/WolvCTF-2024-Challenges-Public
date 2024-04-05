out=b'\x14\x5D\x14\x57\x16\x43\x46\x7A\x56\x16\x57\x17\x4B\x16\x52\x4C\x61\x1C\x1C\x7A\x1D\x7A\x11\x51\x52\x16\x5E\x62\x6D\x5E\x61\x7A\x16\x17\x61\x16\x6B\x61\x4E\x69\x14\x6B\x6D\x51\x57\x6D\x6D\x58\x5D\x4B'

def swap(a, i1, i2):
    a[i1], a[i2] = a[i2], a[i1]

out = list(out)
print(out)

for i in range(49,-1,-1):
    swap(out,i,((i+83)*12)%50)
for i in range(49,-1,-1):
    out[i] =0x5 ^ out[i]
    out[i] =0x20 ^ out[i]
for i in range(49,-1,-1):
    swap(out,i,((i+3)*7)%50)
for i in range(49,-1,-1):
    swap(out,i,((i+7)*15)%50)

for c in out:
    print(chr(c),end='')
print()