from multiply import *
from itertools import tee
import time


def mul_py(a, b):
    b_iter = tee(zip(*b), len(a))
    return [
        [
            sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
            for col_b in b_iter[i]
        ] for i, row_a in enumerate(a)
    ]


if __name__ == '__main__':
    x = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    y = [[1, 2], [1, 2], [3, 4]]
    start_py = time.time()
    mul_py(x, y)
    end_py = time.time()
    time_py = end_py - start_py

    start_c = time.time()
    mul_c(x, y)
    end_c = time.time()
    time_c = end_c - start_c
    print(f'time_py={time_py}, time_c={time_c}')
