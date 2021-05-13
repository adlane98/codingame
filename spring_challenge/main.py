import sys
import math
from enum import Enum
import random


def debug(x):
    print(x, file=sys.stderr)


def get_richness_from_index(index):
    if index in range(0, 7):
        return 3
    elif index in range(7, 19):
        return 2
    elif index in range(19, 37):
        return 2
    else:
        raise Exception("Wrong index")


def get_cell(game, cell_index):
    return [c for c in game.board if c.index == cell_index][0]


def get_tree_from_cell(game, cell):
    if type(cell) == Cell:
        return [t for t in game.trees if t.cell.index == cell.index][0]
    else:
        return [t for t in game.trees if t.cell.index == cell][0]


class Cell:
    def __init__(self, cell_index, richness, neighbors):
        self.index = cell_index
        self.richness = richness
        self.neighbors = neighbors

    def get_lvl1_coverage(self, game):
        level1_neighbors = [n for n in self.neighbors if
                            get_cell(game, n).richness > 0]
        return len(set(level1_neighbors))

    def get_lvl2_coverage(self, game):
        level1_neighbors = [n for n in self.neighbors if
                            get_cell(game, n).richness > 0]
        total_neighbors = level1_neighbors.copy()
        for nb in level1_neighbors:
            level1_neighboor_cell = get_cell(game, nb)
            level2_neighboor_cell = [n for n in level1_neighboor_cell.neighbors
                                     if get_cell(game, n).richness > 0]
            total_neighbors.extend(level2_neighboor_cell)

        return len(set(total_neighbors))

    def get_lvl3_coverage(self, game):
        level1_neighbors = [n for n in self.neighbors if get_cell(game, n).richness > 0]

        total_neighbors = level1_neighbors.copy()
        for nb in level1_neighbors:
            level1_neighboor_cell = get_cell(game, nb)
            level2_neighboor_cell = [n for n in level1_neighboor_cell.neighbors if get_cell(game, n).richness > 0]
            total_neighbors.extend(level2_neighboor_cell)

        level2_neighboors = total_neighbors.copy()
        for nb in level2_neighboors:
            level2_neighboor_cell = get_cell(game, nb)
            level3_neighboor_cell = [n for n in level2_neighboor_cell.neighbors
                                     if get_cell(game, n).richness > 0]
            total_neighbors.extend(level3_neighboor_cell)

        print(f"total_neigh = {set(total_neighbors)}", file=sys.stderr)
        return len(set(total_neighbors))


class Tree:
    def __init__(self, cell, size, is_mine, is_dormant):
        self.cell = cell
        self.size = size
        self.is_mine = is_mine
        self.is_dormant = is_dormant


class ActionType(Enum):
    WAIT = "WAIT"
    SEED = "SEED"
    GROW = "GROW"
    COMPLETE = "COMPLETE"


def debug_seed_score(game, max_surface_to_cover, seed_first_turn,
                     sun_cost, target_cell_richness):
    print(game.nutrients, file=sys.stderr)
    print(target_cell_richness, file=sys.stderr)
    print(max_surface_to_cover, file=sys.stderr)
    print(seed_first_turn, file=sys.stderr)
    print(game.my_sun, file=sys.stderr)
    print(sun_cost, file=sys.stderr)


class Action:
    def __init__(self, type, target_cell_id=None, origin_cell_id=None):
        self.type = type
        self.target_cell_id = target_cell_id
        self.origin_cell_id = origin_cell_id

    def __str__(self):
        if self.type == ActionType.WAIT:
            return 'WAIT'
        elif self.type == ActionType.SEED:
            return f'SEED {self.origin_cell_id} {self.target_cell_id}'
        else:
            return f'{self.type.name} {self.target_cell_id}'

    def __eq__(self, other):
        return self.type == other.type \
               and self.target_cell_id == other.target_cell_id \
               and self.origin_cell_id == other.origin_cell_id

    def get_score(self, game, seed_first_turn):
        if self.type == ActionType.SEED:
            target_cell = get_cell(game, self.target_cell_id)
            sun_cost = game.get_nb_seeds()
            target_cell_richness = target_cell.richness
            max_surface_to_cover = target_cell.get_lvl3_coverage(game)
            return game.nutrients + target_cell_richness + max_surface_to_cover - (seed_first_turn - game.my_sun) - sun_cost

        elif self.type == ActionType.GROW:
            target_cell = get_cell(game, self.target_cell_id)
            tree = get_tree_from_cell(game, target_cell)
            additional_cost = 1 if tree.size == 0 else (3 if tree.size == 1 else 7)
            sun_cost = game.get_nb_trees(tree.size + 1) + additional_cost
            target_cell_richness = target_cell.richness

            if tree.size == 0:
                coverage_diff = target_cell.get_lvl1_coverage()
                additional_cost = 1
            elif tree.size == 1:
                coverage_diff = target_cell.get_lvl2_coverage() - target_cell.get_lvl1_coverage()
                additional_cost = 3
            else:
                coverage_diff = target_cell.get_lvl3_coverage() - target_cell.get_lvl2_coverage()
                additional_cost = 7

    @staticmethod
    def parse(action_string):
        split = action_string.split(' ')
        if split[0] == ActionType.WAIT.name:
            return Action(ActionType.WAIT)
        if split[0] == ActionType.SEED.name:
            return Action(ActionType.SEED, int(split[2]), int(split[1]))
        if split[0] == ActionType.GROW.name:
            return Action(ActionType.GROW, int(split[1]))
        if split[0] == ActionType.COMPLETE.name:
            return Action(ActionType.COMPLETE, int(split[1]))


class Game:
    def __init__(self):
        self.day = 0
        self.nutrients = 0
        self.board = []
        self.trees = []
        self.possible_actions = []
        self.my_sun = 0
        self.my_score = 0
        self.opponents_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = 0

    def compute_next_action(self):
        return self.possible_actions[0]

    def get_trees(self, level):
        return [seed for seed in self.trees if seed.size == level]

    def get_seeds(self):
        return self.get_trees(0)

    def get_nb_trees(self, level):
        return len(self.get_trees(level))

    def get_nb_seeds(self):
        return self.get_nb_trees(0)


def get_action_string(action):
    return action.__str__()


def get_richness_from_tree(tree):
    return tree.cell.richness


if __name__ == '__main__':

    number_of_cells = int(input())
    game = Game()
    for i in range(number_of_cells):
        cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [
            int(j) for j in input().split()]
        neighbors = [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]
        neighbors = [n for n in neighbors if n != -1]
        game.board.append(Cell(cell_index, richness, neighbors))

    while True:
        _day = int(input())
        game.day = _day

        nutrients = int(input())
        game.nutrients = nutrients

        sun, score = [int(i) for i in input().split()]
        game.my_sun = sun
        game.my_score = score

        opp_sun, opp_score, opp_is_waiting = [int(i) for i in input().split()]
        game.opponent_sun = opp_sun
        game.opponent_score = opp_score
        game.opponent_is_waiting = opp_is_waiting

        number_of_trees = int(input())
        game.trees.clear()

        for i in range(number_of_trees):
            inputs = input().split()
            cell = get_cell(game, int(inputs[0]))
            size = int(inputs[1])
            is_mine = inputs[2] != "0"
            is_dormant = inputs[3] != "0"
            game.trees.append(Tree(cell, size, is_mine == 1, is_dormant))

        number_of_possible_actions = int(input())
        game.possible_actions.clear()
        for i in range(number_of_possible_actions):
            possible_action = Action.parse(input())
            game.possible_actions.append(possible_action)

        nb_sun_first_turn = game.my_sun
        for act in game.possible_actions:
            print(f"{act}: {act.get_score(game, nb_sun_first_turn)}", file=sys.stderr)
