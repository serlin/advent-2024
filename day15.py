import string
import re
import copy
import functools
import itertools
from functools import cache
from functools import cmp_to_key
from operator import mul
from operator import add
from enum import Enum
import numpy as np
import aocd
from math import isclose
from time import sleep

data = aocd.get_data(day=15, year=2024)

sample = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

# data = sample

map = data.split("\n\n")[0].splitlines()
commands = data.split("\n\n")[1].replace("\n", "")
# lines = data.splitlines()
robot_loc = (-1, -1)

all_cells = {} #(x,y), Cell

print(map)
print(commands)

max_x = len(map[0])
max_y = len(map)

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class Cell:
    global all_cells
    global max_x
    global max_y
    def __init__(self, location, chr):
        self.chr = chr
        if chr == "@":
            self.chr = "."
        self.location = location
        self.neighbors = set() # Cell

    def __str__(self):
        return f'{self.location}: {self.chr}'
    
    def __repr__(self):
        return f'{self.location}: {self.chr}'
    

    def east_neighbor(self):
        new_loc = (self.location[0]+1, self.location[1])
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None
        
    def west_neighbor(self):
        new_loc = (self.location[0]-1, self.location[1])
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None

    def north_neighbor(self):
        new_loc = (self.location[0], self.location[1]-1)
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None

    def south_neighbor(self):
        new_loc = (self.location[0], self.location[1]+1)
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None
        
    def can_move(self, direction, sender_chr):
        print(direction, ":", sender_chr)
        if self.chr == "#":
            # It's a wall, it can't move
            return False
        elif self.chr == ".":
            self.chr = sender_chr
            return True
        elif self.chr == "O":
            print("found barrel at: ", self.location)
            match direction:
                case Direction.EAST:
                    if self.east_neighbor().can_move(direction, self.chr):
                        self.chr = sender_chr
                        return True
                case Direction.WEST:
                    if self.west_neighbor().can_move(direction, self.chr):
                        self.chr = sender_chr
                        return True
                case Direction.NORTH:
                    if self.north_neighbor().can_move(direction, self.chr):
                        self.chr = sender_chr
                        return True
                case Direction.SOUTH:
                    if self.south_neighbor().can_move(direction, self.chr):
                        self.chr = sender_chr
                        return True
        else:
            print("WTAF")
            return("WTAF")


def draw_grid():
    print("----------------------------------------------------------------------------------")
    for y in range(0, max_y):
        print("")
        for x in range(0, max_x):
            if (x,y) == robot_loc:
                print("@", end='')
            else: 
                print(all_cells[(x, y)].chr, end='')
    print("\n----------------------------------------------------------------------------------")




for idx, line in enumerate(map):
    match = re.search("@", line)
    if match:
        print("found robot at: ", match.start(), ":", idx)
        robot_loc = (match.start(), idx)

for y, line in enumerate(map):
    for x, chr in enumerate(line):
        all_cells[(x,y)] = Cell((x, y), chr)

print(all_cells)
print("----------------------------")
draw_grid()

for command in commands:
    curr_cell = all_cells[robot_loc]
    print(robot_loc, ":", command)
    match command:
        case "<":
            if curr_cell.west_neighbor().can_move(Direction.WEST, curr_cell.chr):
                robot_loc = (robot_loc[0] - 1, robot_loc[1])
                curr_cell.chr = "."
            else:
                pass
        case ">":
            if curr_cell.east_neighbor().can_move(Direction.EAST, curr_cell.chr):
                robot_loc = (robot_loc[0] + 1, robot_loc[1])
                curr_cell.chr = "."
            else:  
                pass    
        case "^":
            if curr_cell.north_neighbor().can_move(Direction.NORTH, curr_cell.chr):
                robot_loc = (robot_loc[0], robot_loc[1] - 1)
                curr_cell.chr = "."
            else:  
                pass    
        case "v":
            if curr_cell.south_neighbor().can_move(Direction.SOUTH, curr_cell.chr):
                robot_loc = (robot_loc[0], robot_loc[1] + 1)
                curr_cell.chr = "."
            else:  
                pass
    draw_grid()
    # sleep(1)

total = 0

for y in range(0, max_y):
    for x in range(0, max_x):
        cell = all_cells[(x, y)]
        if cell.chr == "O":
            total += y * 100 + x

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="a", day=15, year=2024)
