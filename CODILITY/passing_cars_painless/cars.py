# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

import random
import time


def solution(A):
    # write your code in Python 3.6
    pairs_num = 0
    east = 0
    for i in range(len(A)):
        if A[i]:
            pairs_num += east
        else:
            east += 1
        if pairs_num > 1_000_000_000:
            return -1
    return pairs_num


if __name__ == "__main__":
    for test in range(8):
        A = [random.randint(0, 1) for _ in range(random.randint(99999, 100000))]
        # print(A)
        print('A len: ', len(A))
        start = time.time()
        print(solution(A))
        finish = time.time()
        print(f'Elapsed time: {finish - start}')

    # start = time.time()
    # print(solution([0, 1, 0, 1, 1]))
    # finish = time.time()
    # print(f'Elapsed time: {finish - start}')
