import numpy as np


'''
a b c d
e f g h
i j k l
m n o p
'''


def check_a(grid):
    return True


def check_b(grid):
    return grid[0, 0] + grid[0, 1] <= 12


def check_c(grid):
    return grid[0, 0] + grid[0, 1] + grid[0, 2] <= 12


def check_d(grid):
    return np.sum(grid[0, :]) == 12


def check_e(grid):
    return grid[0, 0] + grid[1, 0] <= 12


def check_i(grid):
    return grid[2, 0] + grid[1, 0] + grid[0, 0] <= 12


def check_m(grid):
    return np.sum(grid[:, 0]) == 12 and grid[3, 0] + grid[0, 3] <= 12


def check_f(grid):
    return grid[1, 0] + grid[1, 1] <= 12 \
           and grid[0, 0] + grid[1, 1] <= 12 \
           and grid[0, 1] + grid[1, 1] <= 12


def check_j(grid):
    return grid[2, 0] + grid[2, 1] <= 12 \
           and grid[0, 1] + grid[1, 1] + grid[2, 1] <= 12 \
           and grid[0, 3] + grid[2, 1] + grid[3, 0] <= 12


def check_n(grid):
    return grid[3, 0] + grid[3, 1] <= 12 \
           and np.sum(grid[:, 1]) == 12


def check_g(grid):
    return grid[1, 0] + grid[1, 1] + grid[1, 2] <= 12 \
           and grid[0, 2] + grid[1, 2] <= 12 \
           and grid[0, 3] + grid[1, 2] + grid[2, 1] + grid[3, 0] == 12


def check_h(grid):
    return np.sum(grid[1, :]) == 12 \
           and grid[0, 3] + grid[1, 3] <= 12


def check_k(grid):
    return grid[2, 0] + grid[2, 1] + grid[2, 2] <= 12 \
           and grid[0, 2] + grid[1, 2] + grid[2, 2] <= 12 \
           and grid[0, 0] + grid[1, 1] + grid[2, 2] <= 12


def check_l(grid):
    return np.sum(grid[2, :]) == 12 \
           and grid[0, 3] + grid[1, 3] + grid[2, 3] <= 12


def check_o(grid):
    return grid[3, 0] + grid[3, 1] + grid[3, 2] <= 12 \
           and np.sum(grid[:, 2]) == 12


def check_p(grid):
    return np.sum(grid[3, :]) == 12 \
           and np.sum(grid[:, 3]) == 12 \
           and np.trace(grid) == 12


checkers_funs = [
    check_a,
    check_b,
    check_c,
    check_d,
    check_e,
    check_i,
    check_m,
    check_f,
    check_j,
    check_n,
    check_g,
    check_h,
    check_k,
    check_l,
    check_o,
    check_q,
]