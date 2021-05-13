import math


class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.letter = None
        self.p1_score = None
        self.p2_score = None
        self.diff_score = None


def evaluate(player_letters, scores_dict):
    total = 0
    for word_letters, score in scores_dict.items():
        if all(letter in player_letters for letter in word_letters):
            total += score
    return total


def build_tree(game_tree, remaining_letters, p1_letters, p2_letters, turn,
               scores_dict, current_letter):
    """

    :param game_tree:
    :param remaining_letters:
    :param p1_letters:
    :param p2_letters:
    :param turn: True if p1 plays else false
    :return:
    """
    if len(remaining_letters) == 0:
        game_tree.letter = current_letter
        game_tree.p1_score = evaluate(p1_letters + turn * [current_letter], scores_dict)
        game_tree.p2_score = evaluate(p2_letters + (not turn) * [current_letter], scores_dict)
        game_tree.diff_score = game_tree.p1_score - game_tree.p2_score

        return game_tree.diff_score

    elif len(remaining_letters) == 1:
        extr_score = -math.inf if turn else math.inf
        extr_fun = max if turn else min

        game_tree.letter = current_letter

        game_tree.left = Tree()
        next_letter = remaining_letters[0]

        new_score = build_tree(
            game_tree.left,
            remaining_letters[1:],
            p1_letters + turn * [current_letter],
            p2_letters + (not turn) * [current_letter],
            not turn,
            scores_dict,
            next_letter
        )
        extr_score = extr_fun(extr_score, new_score)
        game_tree.diff_score = extr_score

        game_tree.diff_score = extr_score
        return extr_score

    else:
        extr_score = -math.inf if turn else math.inf
        extr_fun = max if turn else min

        game_tree.letter = current_letter

        game_tree.left = Tree()
        next_letter = remaining_letters[0]
        new_score = build_tree(
            game_tree.left,
            remaining_letters[1:],
            p1_letters + turn * [current_letter],
            p2_letters + (not turn) * [current_letter],
            not turn,
            scores_dict,
            next_letter
        )
        extr_score = extr_fun(extr_score, new_score)

        game_tree.right = Tree()
        next_letter = remaining_letters[1]

        if len(remaining_letters) > 2:
            new_letters = [remaining_letters[0]] + remaining_letters[2:]
        else:
            new_letters = [remaining_letters[0]]

        new_score = build_tree(
            game_tree.right,
            new_letters,
            p1_letters + turn * [current_letter],
            p2_letters + (not turn) * [current_letter],
            not turn,
            scores_dict,
            next_letter
        )
        extr_score = extr_fun(extr_score, new_score)
        game_tree.diff_score = extr_score
        return extr_score


def minimax(sub_tree, alpha, beta, turn):
    if sub_tree.left is None:
        return sub_tree.diff_score

    elif turn:
        max_score = -math.inf

        new_score = minimax(sub_tree.left, alpha, beta, False)
        max_score = max(max_score, new_score)

        alpha = max(alpha, max_score)

        if sub_tree.right is not None and beta > alpha:
            new_score = minimax(sub_tree.right, alpha, beta, False)
            max_score = max(max_score, new_score)
        else:
            sub_tree.right = None

        sub_tree.diff_score = max_score
        return max_score

    else:
        min_score = math.inf

        new_score = minimax(sub_tree.left, alpha, beta, True)
        min_score = min(min_score, new_score)

        beta = min(beta, min_score)

        if sub_tree.right is not None and beta > alpha:
            new_score = minimax(sub_tree.right, alpha, beta, True)
            min_score = min(min_score, new_score)
        else:
            sub_tree.right = None

        sub_tree.diff_score = min_score
        return min_score


def get_final_score(sub_tree, turn):
    if sub_tree.left is None:
        return sub_tree.p1_score, sub_tree.p2_score
    elif sub_tree.right is None:
        return get_final_score(sub_tree.left, not turn)
    elif turn:
        if sub_tree.left.diff_score >= sub_tree.right.diff_score:
            return get_final_score(sub_tree.left, not turn)
        else:
            return get_final_score(sub_tree.right, not turn)
    else:
        if sub_tree.left.diff_score <= sub_tree.right.diff_score:
            return get_final_score(sub_tree.left, not turn)
        else:
            return get_final_score(sub_tree.right, not turn)


def get_first_letter(gt):
    if gt.left.diff_score >= gt.right.diff_score:
        return gt.left.letter
    else:
        return gt.right.letter


if __name__ == '__main__':

    n, q = [int(i) for i in input().split()]
    letters = input().split()

    for letter in letters:
        pass

    scores_dict = dict()
    for i in range(q):
        inputs = input().split()
        word = inputs[0]
        score = int(inputs[1])
        scores_dict[word] = score

    # Write an answer using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    game_tree = Tree()

    p1_letters = []
    p2_letters = []
    build_tree(game_tree, letters, p1_letters, p2_letters, False, scores_dict, None)


    print(scores_dict)
    print("choice score1-score2")
    # print(minimax(game_tree, -math.inf, math.inf, True))

    print(get_first_letter(game_tree))
    print(get_final_score(game_tree, True))

"""
def build_tree(game_tree, remaining_letters, p1_letters, p2_letters, turn,
               scores_dict):

    :param game_tree:
    :param remaining_letters:
    :param p1_letters:
    :param p2_letters:
    :param turn: True if p1 plays else false
    :return:

    if len(remaining_letters) == 1:
        game_tree.left = Tree()
        game_tree.left.letter = remaining_letters[0]

        game_tree.left.p1_score = evaluate(
            p1_letters + turn * [remaining_letters[0]], scores_dict)
        game_tree.left.p2_score = evaluate(
            p2_letters + (not turn) * [remaining_letters[0]], scores_dict)
        game_tree.left.diff_score = game_tree.left.p1_score - game_tree.left.p2_score


    else:
        game_tree.left = Tree()
        game_tree.left.letter = remaining_letters[0]
        build_tree(
            game_tree.left,
            remaining_letters[1:],
            p1_letters + turn * [remaining_letters[0]],
            p2_letters + (not turn) * [remaining_letters[0]],
            not turn,
            scores_dict
        )

        game_tree.right = Tree()
        game_tree.right.letter = remaining_letters[1]

        if len(remaining_letters) > 2:
            new_letters = [remaining_letters[0]] + remaining_letters[2:]
        else:
            new_letters = remaining_letters[0]

        build_tree(
            game_tree.right,
            new_letters,
            p1_letters + turn * [remaining_letters[1]],
            p2_letters + (not turn) * [remaining_letters[1]],
            not turn,
            scores_dict
        )
"""