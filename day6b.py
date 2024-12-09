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

# data = sample

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

lines = data.splitlines()
curr_loc = (-1,-1)
curr_dir = Direction.NORTH
all_locs = set()
all_locs_with_dir = set()
btotal = 0


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
        return True

def check_collision(loc, dir):
    step = loc
    while is_in_grid(step[0], step[1]):
        print ("checking for collision", step, dir)
        match dir:
            case Direction.NORTH:
                step = (step[0], step[1] - 1)
            case Direction.EAST:
                step = (step[0] + 1, step[1])
            case Direction.SOUTH:
                step = (step[0], step[1] + 1)
            case Direction.WEST:
                step = (step[0] - 1, step[1])
        if not is_in_grid(step[0], step[1]) or lines[step[1]][step[0]] == "#":
            return False
        if (step, dir) in all_locs_with_dir:
            print("Found match")
            return True
    return False

def walk():
    global curr_loc
    global btotal
    next_loc = next_step(curr_dir)
    next_chr = lines[next_loc[1]][next_loc[0]]
    if next_chr == "." or next_chr == "^":
        if (next_step(next_face()), next_face()) in all_locs_with_dir: #Find the immediate neighbours but not the long distance ones
            print("found possible neighbor barrel at", curr_loc)
            btotal += 1
        elif check_collision(curr_loc, next_face()):
            print("found possible long barrel at", curr_loc)
            btotal += 1
        all_locs.add(curr_loc)
        all_locs_with_dir.add((curr_loc, curr_dir))
        curr_loc = next_loc
    else:
        all_locs_with_dir.add((curr_loc, curr_dir))
        change_face()
        all_locs_with_dir.add((curr_loc, curr_dir))
    
# While current loc is within the bound of the grid ... walk()

while is_in_grid(next_step(curr_dir)[0], next_step(curr_dir)[1]):
    print("at", curr_loc, "facing", curr_dir)
    walk()

# maybe just insert a barrel everywhere and see if anything works?



all_locs.add(curr_loc)
total = len(all_locs)

print ("Total is: ", btotal, "submitting...")
# aocd.submit(btotal, part="b", day=6, year=2024)