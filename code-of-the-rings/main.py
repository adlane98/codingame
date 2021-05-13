import sys
import math

N = 30

runes = [' '] * N
rune_ptr = 0


def inc_rune_ptr():
    global rune_ptr
    rune_ptr = (rune_ptr + 1) % N

def dec_rune_ptr():
    global rune_ptr
    rune_ptr = (rune_ptr - 1) % N

def charid(character):
    if character == ' ':
        return 0
    else:
        return ord(character) - ord('A') + 1


def modular_distance(a, b, m):
    sense = (a - b) % m > (b - a) % m
    return min((a - b) % m, (b - a) % m), sense


def rune_distance(rune_id1, rune_id2):
    res, sense = modular_distance(rune_id1, rune_id2, N)
    return res, '>' if sense else '<'


def char_distance(letter_id1, letter_id2):
    res, sense = modular_distance(letter_id1, letter_id2, 27)
    return res, "+" if sense else "-"


def stay_mode(id_rune_letter, id_next_letter):
    nb_update, sense = char_distance(id_rune_letter, id_next_letter)
    return sense * nb_update


def move_mode(id_next_letter):
    min_nb_actions = math.inf
    min_actions = ''
    min_tmp_rune_ptr = rune_ptr
    for tmp_rune_ptr in range(N):
        rune_dist, sense = rune_distance(rune_ptr, tmp_rune_ptr)
        if rune_dist > min_nb_actions:
            continue

        actions = sense * rune_dist

        char_dist, sense = char_distance(
            charid(runes[tmp_rune_ptr]), id_next_letter
        )
        nb_actions = char_dist + rune_dist
        if nb_actions < min_nb_actions:
            min_nb_actions = nb_actions
            sense = '+' if sense else '-'
            min_tmp_rune_ptr = tmp_rune_ptr
            min_actions = actions + sense * char_dist

    return min_actions, min_tmp_rune_ptr


def init_pattern(pattern):
    actions = ""
    for letter in pattern:
        char_dist, sense = char_distance(charid(runes[rune_ptr]), charid(letter))
        actions += sense * char_dist
        actions += ">"
        inc_rune_ptr()

    return actions


def set_counter(nb_pattern_repeat):
    actions = ""
    res, sense = char_distance(charid(runes[rune_ptr]), 26 - nb_pattern_repeat)
    actions += sense * res
    return actions


def make_loop(pattern):
    actions = "["
    actions += "<" * len(pattern)
    actions += ".>" * len(pattern)
    actions += "+"
    actions += "]"
    return actions


if __name__ == '__main__':

    # magic_phrase = input()
    # actions = ""
    #
    # for letter in magic_phrase:
    #     # actions += stay_mode(charid(runes[rune_ptr]), charid(letter))
    #     new_actions_sm = stay_mode(charid(runes[rune_ptr]), charid(letter))
    #     new_actions_mm, new_rp = move_mode(charid(letter))
    #
    #     actions += (new_actions_sm if len(new_actions_sm) < len(new_actions_mm) else new_actions_mm) + "."
    #     rune_ptr = rune_ptr if len(new_actions_sm) < len(new_actions_mm) else new_rp
    #     runes[rune_ptr] = letter
    #
    # print(actions)
    p = "ACQGA"
    print(init_pattern(p) + set_counter(3) + make_loop(p))


# "+.>-."

