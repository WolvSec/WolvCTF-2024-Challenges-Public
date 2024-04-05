import random


if __name__ == '__main__':
    flag = "wctf"+ "{" + "f34R_0f_m1ss1ng_0ut" + "}"
    print(flag)
    flag = flag.encode('utf-8')
    correct = []
    time_cycle = random.randint(0, 255)
    for i in range(len(flag)):
        random.seed(i+time_cycle)
        correct.append(flag[i] ^ random.getrandbits(8))
    print("Time Cycle")
    print(time_cycle)
    print("correct")
    print(correct)

    