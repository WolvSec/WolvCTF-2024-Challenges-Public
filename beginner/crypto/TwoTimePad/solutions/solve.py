with(open('eWolverine.bmp', 'rb')) as f:
    wolverine = f.read()
with(open('eFlag.bmp', 'rb')) as f:
    flag = f.read()

with(open('sol.bmp', 'wb')) as f:
    f.write(wolverine[:55])
    for i in range(55, len(wolverine), 16):
        f.write(bytes(a^b for a, b in zip(wolverine[i:i+16], flag[i:i+16])))

# wctf{D0NT_R3CYCLE_K3Y5}