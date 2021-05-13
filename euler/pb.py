import numpy as np
from enum import Enum

from checkers import checkers_funs


class Level(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    I = 5
    M = 6
    F = 7
    J = 8
    N = 9
    G = 10
    H = 11
    K = 12
    L = 13
    O = 14
    P = 15


coords = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 0),
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (3, 0),
    (3, 1),
    (3, 2),
    (3, 3)
]

valid_grid = {}


class Tree:
    def __init__(self, grid, level):
        self.children = [None] * 10
        self.grid = grid


def dfs_tree(level, tree):
    c = coords[level]
    check = checkers_funs[level]

    if level == 15:
        for i in range(10):
            tree.grid[c[0], c[1]] = i
            if check(tree.grid):
                valid_grid[str(tree.grid)] = True



def display_grid(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            print(grid[i, j], end=' ')
        print()


def symsrots(grid):
    rot_90 = np.rot90(grid)
    rot_180 = np.rot90(rot_90)
    rot_270 = np.rot90(rot_180)
    sym_v = np.flip(grid, axis=0)
    sym_h = np.flip(grid, axis=1)
    sym_v_rot_90 = np.flip(rot_90, axis=0)
    sym_h_rot_90 = np.flip(rot_90, axis=1)
    sym_v_rot_180 = np.flip(rot_180, axis=0)
    sym_h_rot_180 = np.flip(rot_180, axis=1)
    sym_v_rot_270 = np.flip(rot_270, axis=0)
    sym_h_rot_270 = np.flip(rot_270, axis=1)
    transpose = np.transpose(grid)
    return (
        rot_90,
        rot_180,
        rot_270,
        sym_v,
        sym_h,
        sym_v_rot_90,
        sym_h_rot_90,
        sym_v_rot_180,
        sym_h_rot_180,
        sym_v_rot_270,
        sym_h_rot_270,
        transpose
    )


def check_grid(grid):
    vec_12 = np.array([12, 12, 12, 12])
    assert all(np.sum(grid, axis=0) == vec_12)
    assert all(np.sum(grid, axis=1) == vec_12)
    assert np.trace(grid) == 12
    assert np.trace(np.fliplr(grid)) == 12


def check_still_good_grid(grid):
    vec_12 = np.array([12, 12, 12, 12])
    assert all(np.sum(grid, axis=0) <= vec_12)
    assert all(np.sum(grid, axis=1) <= vec_12)
    assert np.trace(grid) <= 12
    assert np.trace(np.fliplr(grid)) <= 12


def grid_to_string(grid):
    res = ""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            res += str(grid[i, j])

    return res


if __name__ == '__main__':

    letters_grid = np.array([
        ['a', 'b', 'c', 'd'],
        ['e', 'f', 'g', 'h'],
        ['i', 'j', 'k', 'l'],
        ['m', 'n', 'o', 'p']
    ])

    nb_grid = np.array([
        [6, 3, 3, 0],
        [5, 0, 4, 3],
        [0, 7, 1, 4],
        [1, 2, 4, 5]
    ])

    display_grid(nb_grid)
    print("----------")
    for g in symsrots(nb_grid):
        check_grid(g)
        display_grid(g)
        print(grid_to_string(g))
        print("----------")