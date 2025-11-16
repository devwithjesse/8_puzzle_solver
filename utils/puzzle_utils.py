# Helpers for 8-puzzle states
from typing import List, Tuple

def state_from_entries(values: List[List[str]]):
    # values: 3x3 list of strings from input entries
    flat = []
    for row in values:
        for v in row:
            if v == '':
                raise ValueError('All tiles must be filled with numbers 0-8.')
            try:
                n = int(v)
            except:
                raise ValueError('Tiles must be integers from 0 to 8.')
            flat.append(n)
    if len(flat) != 9:
        raise ValueError('Expected 9 values.')
    if sorted(flat) != list(range(9)):
        raise ValueError('Tiles must be numbers 0 through 8 with no repetition.')
    return tuple(flat)

def validate_state(state):
    return isinstance(state, tuple) and len(state) == 9 and sorted(state) == list(range(9))

def is_goal(state, goal):
    return state == goal

def neighbors(state):
    # yields (new_state, move_description)
    s = list(state)
    i = s.index(0)
    r, c = divmod(i, 3)
    moves = []
    def swap_and_make(newi, action):
        ns = s.copy()
        ns[i], ns[newi] = ns[newi], ns[i]
        return (tuple(ns), action)

    if r > 0:  # up
        newi = (r-1)*3 + c
        moves.append(swap_and_make(newi, f'Move {s[newi]} down'))
    if r < 2:  # down
        newi = (r+1)*3 + c
        moves.append(swap_and_make(newi, f'Move {s[newi]} up'))
    if c > 0:  # left
        newi = r*3 + (c-1)
        moves.append(swap_and_make(newi, f'Move {s[newi]} right'))
    if c < 2:  # right
        newi = r*3 + (c+1)
        moves.append(swap_and_make(newi, f'Move {s[newi]} left'))

    return moves


