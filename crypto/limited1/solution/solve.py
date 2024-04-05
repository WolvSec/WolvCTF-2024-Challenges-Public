import random

if __name__ == '__main__':
    correct = correct = [189, 24, 103, 164, 36, 233, 227, 172, 244, 213, 61, 62, 84, 124, 242, 100, 22, 94, 108, 230, 24, 190, 23, 228, 24]
    for time_cycle in range(256):
        print(time_cycle)
        # Actual for reference
        # time_cycle = 188
        flag = []
        for i in range(len(correct)):
            random.seed(i+ time_cycle)
            flag.append(correct[i] ^ random.getrandbits(8))
        flag_print = ''
        for i in flag:
            flag_print = flag_print + chr(i)
        print(flag_print)
