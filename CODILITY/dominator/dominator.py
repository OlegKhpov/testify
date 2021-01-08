import time
import random


def solution(A):
    B = A[:]
    half_length = len(A) // 2
    B.sort()
    dominator = -1
    if A == []:
        return dominator
    candidate = B[half_length]
    count = 0
    for i in range(len(A)):
        if B[i] == candidate:
            count += 1
    if count > half_length:
        dominator = candidate
        return A.index(dominator)
    return dominator


if __name__ == "__main__":
    for test in range(8):
        A = [random.randint(1, 2) for _ in range(random.randint(5, 20))]
        start = time.time()
        print(solution(A))
        finish = time.time()
        print(f'Elapsed time: {finish - start}')
    print(solution([]))
