import sys
import math
from enum import Enum
import random


class Cell:
    def __init__(self, cell_index, richness, neighbors):
        self.cell_index = cell_index
        self.richness = richness
        self.neighbors = neighbors


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
        if self.type == "SEED":
            return game.nutrients + game.richness

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


def get_action_string(action):
    return action.__str__()


def get_cell(game, cell_index):
    return [c for c in game.board if c.index == cell_index][0]


def get_richness_from_tree(tree):
    return tree.cell.richness


if __name__ == '__main__':

    number_of_cells = int(input())
    game = Game()
    for i in range(number_of_cells):
        cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [
            int(j) for j in input().split()]
        game.board.append(Cell(cell_index, richness,
                               [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4,
                                neigh_5]))

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
            possible_action = input()
            game.possible_actions.append(Action.parse(possible_action))

        myTrees = [t for t in game.trees if t.is_mine]
        myTrees = sorted(myTrees, key=get_richness_from_tree, reverse=True)
        for mt in myTrees:
            print(mt.cell.index, file=sys.stderr)

        game.possible_actions = sorted(game.possible_actions,
                                       key=get_action_string)
        for pa in game.possible_actions:
            # print(pa, file=sys.stderr)
            compute_best_actions()

        best_action = f"COMPLETE {myTrees[0].cell.index}"
        if best_action in map(lambda a: a.__str__(), game.possible_actions):
            print(best_action)
        else:
            print(game.possible_actions[0])