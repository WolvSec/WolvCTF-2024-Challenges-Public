# solve.py ~ HCAdam 2024
import struct
from elftools.elf.elffile import ELFFile

# Enabled on all released builds
USE_ENCRYPTED_MEM = True

#default_binpath = "./collateral_damage_beta"
default_binpath = "./collateral_damage"

def u32(x):
    return x & 0xFFFFFFFF

def rotl_u32(x, n):
    return u32((x << n) | (x >> (32 - n)))

def memcrypt(addr):
    c = 0x13371337
    for _ in range(32):
        c = rotl_u32(u32((3*c)+1), addr & 31)
        c ^= u32(c >> 1)
        c = u32(c + (addr << 14))
    return c

def vmcode_gimli(s):
    if len(s) != 12:
        print("ERR: Gimli state must be 12x u32")
        exit(-1)
    # u32's
    x = 0
    y = 0
    z = 0
    # for (round = 24; round > 0; --round)
    for round in range(24, 0, -1):
        for column in range(4):
            x = rotl_u32(s[    column], 24)
            y = rotl_u32(s[4 + column],  9)
            z =          s[8 + column]
            s[8 + column] = x ^ u32(z << 1) ^ u32((y & z) << 2)
            s[4 + column] = y ^ x           ^ u32((x | z) << 1)
            s[    column] = z ^ y           ^ u32((x & y) << 3)
        if (round & 3) == 0:    # small swap
            x = s[0]
            s[0] = s[1]
            s[1] = x
            x = s[2]
            s[2] = s[3]
            s[3] = x
        if (round & 3) == 2:    # big swap
            x = s[0]
            s[0] = s[2]
            s[2] = x
            x = s[1]
            s[1] = s[3]
            s[3] = x
        if (round & 3) == 0:    # add round constant
            s[0] ^= (0x9E377900 | round)
    return s

def vmcode_lfsr_next(seed):
    # 16-bit for easy immediate-mode instructions
    lfsr = seed
    for bit in range(16):
        b = ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5)) & 1
        lfsr = (lfsr >> 1) | (b << 15)
    return lfsr

def vmcode_collatz(x):
    n = 0
    while x > 1:
        if x & 1:
            x = u32((3*x)+1)
        else:
            x = u32(x >> 1)
        n += 1
    return n

def vmcode_get_init_state(seed):
    s = [0]*12
    lfsr = vmcode_lfsr_next(seed)
    for i in range(12):
        v = (lfsr << 16)
        lfsr = vmcode_lfsr_next(lfsr)
        v = v | lfsr
        lfsr = vmcode_lfsr_next(lfsr)
        s[i] = v
    return s

def vmcode_encrypt_input(s, inp):
    vmcode_gimli(s)
    for i in range(32):
        new = s[0] ^ inp[i]
        s[0] = new
        inp[i] = new
        vmcode_gimli(s)
    return inp

def vmcode_string_to_words(f):
    s = []
    for i in range(0, len(f), 4):
        w = ord(f[i])
        w |= ord(f[i+1]) << 8
        w |= ord(f[i+2]) << 16
        w |= ord(f[i+3]) << 24
        s.append(w)
    return s

def decrypt_vmcode_encrypted(s, inp):
    # This code is NOT included in the VM bytecode
    #   and needs to be figured out by player.
    # Here as PoC that decryption is possible!
    vmcode_gimli(s)
    for i in range(32):
        o = s[0] ^ inp[i]
        s[0] = inp[i]
        inp[i] = o
        vmcode_gimli(s)
    return inp


def extract_flag_from_elf(binpath, using_memcrypt):
    with open(binpath, 'rb') as f:
        elf = ELFFile(f)
        dsec = elf.get_section_by_name(".data").data()
    # uint32_t flag_enc[32] array is last 128 bytes of .data section
    enc_flag_swp = dsec[len(dsec)-128:]
    # Undo x86-64 Little-Endian byte order
    flag_enc = []
    for v in struct.iter_unpack('<I', enc_flag_swp):
        if using_memcrypt:
            flag_enc.append(v[0] ^ memcrypt(32+len(flag_enc)))
        else:
            flag_enc.append(v[0])
    return flag_enc

def main():
    print("Solving flag from binary:", default_binpath)
    flag_enc = extract_flag_from_elf(default_binpath, USE_ENCRYPTED_MEM)

    s = vmcode_get_init_state(6502)
    flag_words = decrypt_vmcode_encrypted(s, flag_enc)
    
    flag = ""
    for w in flag_words:
        flag += w.to_bytes(4, 'little').decode('ascii')
    
    print()
    print(flag)

    return

if __name__ == '__main__':
    main()
