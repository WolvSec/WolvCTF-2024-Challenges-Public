import random

if __name__ == '__main__':
    correct = [192, 123, 40, 205, 152, 229, 188, 64, 42, 166, 126, 125, 13, 187, 91]
    flag = []
    time_current = 1704153599 # aka the second before New Year's Day 2024
    for j in range(time_current-87600, time_current+1):
        temp_j = j
        flag = []
        for i in range(len(correct)):
            random.seed(i+ temp_j)
            flag.append(correct[i] ^ random.getrandbits(8))
            temp_j = temp_j + random.randint(1, 60)
        flag_print = ''
        for i in flag:
            flag_print = flag_print + chr(i)
        print(flag_print)