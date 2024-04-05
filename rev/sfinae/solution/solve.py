
import functools

import numpy as np

def gen(a, b, c, num):
  res = []
  for _ in range(num):
    a = (a * 171) % 30269
    b = (b * 172) % 30307
    c = (c * 170) % 30323
    res.append((a + b + c) % 32)
  return res

# Generate the matrix

size = 32
mat = []

gr = gen(12643, 29806, 187, (size + 1) * (size + 1))
gi = gen(3823, 25188, 24854, (size + 1) * (size + 1))

row = []

for i in range(size, 0, -1):
  for j in range(size, 0, -1):
    row.append(gr[i*size+j] + gi[i*size+j] * 1j)
  mat.append(row)
  row = []

# print(mat)

W = np.matrix(mat)
inverse = np.linalg.inv(W)

characters = {
  'a': 0+1j,
  'b': 1+0j,
  'c': 2+0j,
  'd': 1+1j,
  'e': 0+2j,
  'f': 3+0j,
  'g': 2+1j,
  'h': 1+2j,
  'i': 0+3j,
  'j': 4+0j,
  'k': 3+1j,
  'l': 2+2j,
  'm': 1+3j,
  'n': 0+4j,
  'o': 5+0j,
  'p': 4+1j,
  'q': 3+2j,
  'r': 2+3j,
  's': 1+4j,
  't': 0+5j,
  'u': 6+0j,
  'v': 5+1j,
  'w': 4+2j,
  'x': 3+3j,
  'y': 2+4j,
  'z': 1+5j,
  '0': 0+6j,
  '1': 7+0j,
  '2': 6+1j,
  '3': 5+2j,
  '4': 4+3j,
  '5': 3+4j,
  '6': 2+5j,
  '7': 1+6j,
  '8': 0+7j,
  '9': 8+0j,
  '_': 7+1j
}

secret = np.array([438+3190j, 102+2664j, 58+2712j, 229+2954j, 219+3452j, 69+2647j, 311+3002j, 303+2647j, 284+2988j, 3+3081j, 830+3274j, -170+2991j, 66+2729j, 123+2948j, 99+2967j, 55+2881j, -50+2920j, 169+3152j, 204+2551j, 328+2709j, -99+2753j, 184+2620j, 165+2893j, 253+2711j, 298+2443j, 195+3000j, 2+2595j, -164+3003j, 555+2977j, -404+2749j, 146+3079j, 283+2578j]).T
secret = secret[::-1]

flag = np.matmul(inverse, secret).reshape((32,)).tolist()[0]

result = ''
for f in flag:
  result += [c for c, v in characters.items() if round(v.real) == round(f.real) and round(v.imag) == round(f.imag)][0]

print(result)
