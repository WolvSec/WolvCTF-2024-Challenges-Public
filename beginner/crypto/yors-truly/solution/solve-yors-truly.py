import base64

plaintext = "A string of text can be encrypted by applying the bitwise XOR operator to every character using a given key"
key = "" # I have lost the key!

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

ciphertext_b64 = base64.b64encode(byte_xor(key.encode(), plaintext.encode()))

ciphertext_decoded = base64.b64decode("NkMHEgkxXjV/BlN/ElUKMVZQEzFtGzpsVTgGDw==")


print(byte_xor(ciphertext_decoded, plaintext.encode()).decode())
# wctf{X0R_i5_f0rEv3r_My_L0Ve}