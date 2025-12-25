"""
this file illustrates the basic usage of the str8ts_solver
"""

from str8ts_solver.output_utils import to_string
from str8ts_solver.solver import solve

# In this example, we will solve this puzzle:
# https://en.wikipedia.org/wiki/File:Str8ts9x9_Gentle_PUZ.png

# We need to provide 3 arguments to the solve function:
# - size - a pair of numbers representing the size of the puzzle,
#   typically (9, 9)
# - blocked - a set of pairs of the "blocked" cells
# - known - a dictionary representing all of the given numbers in the puzzle.
#   Note that they also can be in the blocked fields

# in case of the example puzzles, these arguments look like that:
_SIZE = (9, 9)

# the "upper left corner" of the puzzle has coordinates (0, 0)
_BLOCKED = {
    (0, 0),
    (1, 0),
    (7, 0),
    (8, 0),
    (4, 1),
    (5, 1),
    (3, 2),
    (4, 2),
    (3, 3),
    (7, 3),
    (8, 3),
    (0, 4),
    (8, 4),
    (0, 5),
    (1, 5),
    (5, 5),
    (4, 6),
    (5, 6),
    (3, 7),
    (4, 7),
    (0, 8),
    (1, 8),
    (7, 8),
    (8, 8),
}

_KNOWN = {
    (4, 0): 5,
    (7, 0): 3,
    (1, 1): 6,
    (6, 1): 1,
    (4, 2): 8,
    (0, 3): 9,
    (3, 3): 4,
    (8, 3): 5,
    (5, 4): 3,
    (5, 5): 9,
    (7, 5): 4,
    (0, 6): 4,
    (2, 6): 3,
    (7, 6): 6,
    (2, 7): 1,
    (2, 8): 8,
    (8, 8): 2,
}

# we can inspect the unsolved puzzle by
print("Unsolved puzzle:")
print(to_string(_SIZE, _BLOCKED, _KNOWN, {}))
# note the exclamation marks -
# they indicate that the cell is prefilled with a known value

# now we are ready to call the solve function

_SOLVED = solve(_SIZE, _BLOCKED, _KNOWN)
# if the solution exists, _SOLVED, is a dictionary,
# containing all of the numbers from non-blocked cells
# if a puzzle has no solution, solve function returns None

# in our case, the solution exists
assert _SOLVED is not None

# the value in the cell (3, 1) can be queried using
assert _SOLVED[(3, 1)] == 7
# the _SOLVED does not contain the blocked cells, eg.
assert (0, 0) not in _SOLVED
# but it contains the knowns and non-blocked cells, eg.
assert _SOLVED[(4, 0)] == 5

# one can print the solved puzzle using
print("\n\nsolved puzzle:")
print(to_string(_SIZE, _BLOCKED, _KNOWN, _SOLVED))
