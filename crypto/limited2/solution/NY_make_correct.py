import random
import time


if __name__ == '__main__':
    flag = "wctf"+ "{" + "b4ll_dr0p" + "}"
    print(flag)
    flag = flag.encode('utf-8')
    correct = []
    time_current = 1704153599 # aka the second before New Year's Day 2024
    for i in range(len(flag)):
        random.seed(i+time_current)
        correct.append(flag[i] ^ random.getrandbits(8))
        time_current = time_current + random.randint(1, 60)
    print("correct")
    print(correct)
    # correct = [192, 123, 40, 205, 152, 229, 188, 64, 42, 166, 126, 125, 13, 187, 91]


    
