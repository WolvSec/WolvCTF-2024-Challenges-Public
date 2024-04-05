
flag = b'wctf{pr30ccup13d_w1+h_wh3+h3r_0r_n0t_1_c0uld}'

result = []
p = 101
for i in range(len(flag)):
    k = (p ** i) % 128
    result.append(k ^ flag[i])

print(len(flag))
print(result)

# emit jump table
for n in result:
    print(f'mov 0 {n}')
    print('ret')
