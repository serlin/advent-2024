import string
import re
import copy
import functools
from enum import Enum
import aocd

data = aocd.get_data(day=6, year=2024)

sample = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

data = sample

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


lines = data.splitlines()
curr_loc = (-1,-1)
curr_dir = Direction.NORTH
all_locs = set()



def find_me():
    x = -1
    y = -1
    for idx, line in enumerate(lines):
        if line.find("^") > 0:
            x = line.find("^")
            y = idx
            break
    return (x,y)      


curr_loc = find_me()
print(curr_loc)

def next_step(dir):
    match dir:
        case Direction.NORTH:
            return (curr_loc[0], curr_loc[1] - 1)
        case Direction.EAST:
            return (curr_loc[0] + 1, curr_loc[1])
        case Direction.SOUTH:
            return (curr_loc[0], curr_loc[1] + 1)
        case Direction.WEST:
            return (curr_loc[0] - 1, curr_loc[1])

def next_face():
    global curr_dir
    match curr_dir:
        case Direction.NORTH:
            return Direction.EAST
        case Direction.EAST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.NORTH

def change_face():
    global curr_dir
    match curr_dir:
        case Direction.NORTH:
            curr_dir = Direction.EAST
        case Direction.EAST:
            curr_dir = Direction.SOUTH
        case Direction.SOUTH:
            curr_dir = Direction.WEST
        case Direction.WEST:
            curr_dir = Direction.NORTH

def is_in_grid(x, y):
    if x < 0 or y < 0 or x > len(lines[0]) -1 or y > len(lines) -1:
        return False
    else:
        # print(x, ",", y, "out of grid")
        return True

def walk():
    global curr_loc
    next_loc = next_step(curr_dir)
    next_chr = lines[next_loc[1]][next_loc[0]]
    if next_chr == "." or next_chr == "^":
        if curr_loc in all_locs:
            # standing at an intersection check the one to the right
            check = next_step(next_face())
        all_locs.add(curr_loc)
        curr_loc = next_loc
    else:
        change_face()
    
# While current loc is within the bound of the grid ... walk()

while is_in_grid(next_step()[0], next_step()[1]):
    print("at", curr_loc, "facing", curr_dir)
    walk()

all_locs.add(curr_loc)
total = len(all_locs)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="a", day=6, year=2024)