# Python implementation of Algorithm H for generating Dr. Mario (NES) puzzles.
# Original algorithm written in 6502 assembly by Nintendo's Takahiro Harada.
#
# This implementation is meant to be functionally equivalent to the original.
# For implementations that are closer to the original 6502 assembly see user
# nightmareci's previous C (bottle.c) and C# implementations and comments.
#  - https://tetrisconcept.net/threads/dr-mario-virus-placement.2037/
#  - https://tetris.wiki/Dr._Mario
#  - https://pastebin.com/1fzGA2L8
#
# Also see the article related to this program.
#  - "Dr. Mario Puzzle Generation: Theory, Practice, & History (Famicom/NES)"
#    https://www.researchgate.net/publication/334724493_Dr_Mario_Puzzle_Generation_Theory_Practice_History_FamicomNES
#
# Aaron Williams (July 2019)

from __future__ import print_function
import sys    # command-line arguments
import random # generating a random seed

def random_init(seed):
    global state

    # Convert the decimal value seed into a list of binary bits.
    state = [int(b) for b in bin(seed)[2:]]

    # The state should be 16-bits so pad with a prefix if necessary.
    leading_zeros = 16 - len(state)
    state = leading_zeros*[0] + state

def random_increment():
	global state

	# tap bit 7 and bit 15
	bit9 = state[6]
	bit1 = state[14]
	newbit = bit1 ^ bit9

	# rotate in the new output bit
	state = [newbit] + state[0:15]


def random_row(max_value = 15):
    random_increment()
    value = 8*state[4] + 4*state[5] + 2*state[6] + 1*state[7]
    while value > max_value:
        random_increment()
        value = 8*state[4] + 4*state[5] + 2*state[6] + 1*state[7]
    return value

def random_col():
    value = 4*state[13] + 2*state[14] + 1*state[15]
    return value

def random_index():
    random_increment()
    value = 8*state[12] + 4*state[13] + 2*state[14] + 1*state[15]
    return value

def init(level_num):
    global bottle, bottle_rows, bottle_cols
    set_globals(level_num)
    bottle = [[None for i in range(bottle_cols)] for j in range(bottle_rows)]

def set_globals(level_num):
    global bottle, bottle_rows, bottle_cols, virus_rows, virus_goal

    # Dimensions of the testtube bottle.
    bottle_rows = 16
    bottle_cols = 8

    # TODO this currently assumes level_num = 20
    virus_rows = 13
    virus_goal = 84


def print_bottle():
    global bottle
    for row in reversed(bottle):
        for value in row:
            if value == None: print("-",end="")
            if value == 0: print("Y",end="")
            if value == 1: print("R",end="")
            if value == 2: print("B",end="")
        print("")


# Maximal puzzles are never generated in the NES game.
# It can only occur when increasing the number of viruses beyond the NES game.
def is_maximal():
    global bottle_cols, virus_rows

    # If there is an available color anywhere then the bottle is not maximal.
    for row in range(virus_rows):
        for col in range(bottle_cols):
            if available(row, col) != None:
                return False

    # Otherwise, the bottle is maximal.
    return True


# This bug never occurs in the NES game.
# It can only occur when increasing the number of viruses beyond the NES game.
def is_bug():
    # todo
    return False


def available(row, col):
    # If this cell is already filled then no colors are available.
    if bottle[row][col] != None:
        return set([])

    # Otherwise, initialize the set of available colors.
    colors = set([0,1,2])

    # Remove colors that appear two positions away horizontally or vertically.
    if row-2 >= 0: colors.discard(bottle[row-2][col])
    if col-2 >= 0: colors.discard(bottle[row][col-2])
    if row+2 < virus_rows: colors.discard(bottle[row+2][col])
    if col+2 < bottle_cols: colors.discard(bottle[row][col+2])

    # Return the available colors.
    return colors


# Attempts to add the color with preferred_color (0-based) to position (row, col).
# Returns the color (0-based) that can be assigned.
# Returns None if no color can be assigned.
def add_virus(row, col, preferred_color):
    global bottle, bottle_rows, bottle_cols, virus_rows, virus_goal

    # The sequence of preferred colors (1-based).
    if preferred_color == 0:
        preferred_colors = [0,2,1]
    elif preferred_color == 1:
        preferred_colors = [1,0,2]
    else:
        preferred_colors = [2,1,0]

    # Get the available colors.
    available_colors = available(row, col)

    # Try each color.
    for color in preferred_colors:

        # If this color is not available, then skip over it.
        if color not in available_colors: continue

        # Otherwise, assign the color and return it.
        bottle[row][col] = color
        return color

    # No color was added.
    return None


def fill_bottle():
    global bottle, bottle_rows, bottle_cols, virus_rows, virus_goal

    # Loop until there are no more viruses to be placed.
    num_remaining = virus_goal
    while num_remaining > 0:

        # If the bottle is maximal, then stop trying to fill it.
        # This test is not done in the actual NES game.
        # todo: also test for the bug.
        if is_maximal():
            break

        # Choose an initial random position.
        # Note: Tighter code could be made by doing this inside the next while loop,
        # but the order of random values is very important for accuracy.
        row = random_row(virus_rows-1)
        col = random_col()

        # The preferred color cycles through 0,1,2,_ every four viruses.
        # In the last case it is randomly chosen from a static table.
        preferred_color = num_remaining % 4
        if preferred_color == 3:
            color_table = [0,1,2,2,1,0,0,1,2,2,1,0,0,1,2,1]
            i = random_index()
            preferred_color = color_table[i]

        # Try to add virus at the initial position or later in row-major order.
        while True:

            # Try to add a virus in the current position.
            color_added = add_virus(row, col, preferred_color)

            # If we added a virus, then increment the counter and break the while loop.
            if color_added != None:
                num_remaining -= 1
                break

            # If we have reached the end of the bottle then break to the outer loop.
            if row == 0 and col == bottle_cols-1:
                break

            # Otherwise, move to next position in row-major order.
            col = col + 1
            if col == bottle_cols:
                row = row - 1
                col = 0

    # Return the number of viruses remaining (which is 0 if all were added).
    return num_remaining


if __name__ == "__main__":
    # If 1 parameter is given, then it is just the name of the script.
    # If 2 parameter are given, then the 2nd is the level.
    # If 3 parameters are given, then the 2nd + 3rd are the seed.
    # If 4 parameters are given, then the 2nd is level, and 3rd + 4th the seed.

    # Level: Read from command-line or set to 20 by default.
    if len(sys.argv) == 2:
        level = int(sys.argv[1])
    elif len(sys.argv) == 4:
        level = int(sys.argv[3])
    else:
        level = 20

    # Seed: Read from command-line or randomly generate.
    # s0 s1 are decimal values; seed0 seed1 are hex strings to match bottle.c.
    # https://stackoverflow.com/questions/209513/convert-hex-string-to-int-in-python
    # https://stackoverflow.com/questions/11676864/how-can-i-format-an-integer-to-a-two-digit-hex
    if len(sys.argv) in [3,4]:
        s0 = int(sys.argv[1], 16)
        s1 = int(sys.argv[2], 16)
    else:
        s0 = random.randint(0,255)
        s1 = random.randint(0,255)
    seed0 = "{:02x}".format(s0)
    seed1 = "{:02x}".format(s1)

    # Compute the numeric value of the seed in decimal.
    seed = 256*int(seed0,16) + int(seed1,16)
    random_init(seed)

    print(seed0.upper() + ", " + seed1.upper())
    init(level)
    fill_bottle()
    print_bottle()