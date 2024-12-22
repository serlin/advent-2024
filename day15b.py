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

sample2 = """#######
#...#.#
#.....#
#.....#
#.....#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^^<<^^
"""

data = sample

map = data.split("\n\n")[0].splitlines()
commands = data.split("\n\n")[1].replace("\n", "")
robot_loc = (-1, -1)

all_cells = {} #(x,y), Cell

print(map)
print(commands)

max_x = len(map[0]) * 2
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
    
    def move(self, direction, sender_chr, barrel_call=False):
        print("Move called with: ", self, direction, sender_chr, barrel_call)
        if self.chr == ".":
            print("I should have returned")
            self.chr = sender_chr
            return
        else:
            if self.chr == "[":
                ob = self.east_neighbor()
            elif self.chr == "]":
                ob = self.west_neighbor()
            match direction:
                case Direction.SOUTH:
                    if barrel_call:
                        self.south_neighbor().chr = self.chr
                        self.chr = sender_chr
                    else:
                        self.south_neighbor().move(direction, self.chr)
                        if sender_chr == ".":
                            ob.move(direction, ".", True)
                        elif sender_chr == "]":
                            ob.move(direction, "[", True)
                        elif sender_chr == "[":
                            ob.move(direction, "]", True)
                        self.chr = sender_chr
                case Direction.NORTH:
                    if barrel_call:
                        self.north_neighbor().chr = self.chr 
                        self.chr = sender_chr
                    else:
                        self.north_neighbor().move(direction, self.chr)
                        if sender_chr == ".":
                            ob.move(direction, ".", True)
                        elif sender_chr == "]":
                            ob.move(direction, "[", True)
                        elif sender_chr == "[":
                            ob.move(direction, "]", True)
                        self.chr = sender_chr
                case Direction.WEST:
                    self.west_neighbor().move(direction, self.chr)
                    self.chr = sender_chr
                case Direction.EAST:
                    self.east_neighbor().move(direction, self.chr)
                    self.chr = sender_chr

    def can_move(self, direction, sender_chr, barrel_call=False):
        print(direction, ":", sender_chr)
        if self.chr == "#":
            return False
        elif self.chr == ".":
            return True
        elif self.chr == "[":
            print("found left barrel_call at: ", self.location)
            match direction:
                case Direction.EAST:
                    if self.east_neighbor().can_move(direction, self.chr):
                        return True
                case Direction.WEST:
                    if self.west_neighbor().can_move(direction, self.chr):
                        return True
                case Direction.NORTH:
                    nn = self.north_neighbor()
                    ob = self.east_neighbor()
                    if barrel_call:
                        return nn.can_move(direction, self.chr)
                    else:
                        return nn.can_move(direction, self.chr) and ob.can_move(direction, self.chr, True)
                case Direction.SOUTH:
                    sn = self.south_neighbor()
                    ob = self.east_neighbor()
                    if barrel_call:
                        return sn.can_move(direction, self.chr)
                    else:
                        return sn.can_move(direction, self.chr) and ob.can_move(direction, self.chr, True)
        elif self.chr == "]":
            print("found right barrel_call at: ", self.location)
            match direction:
                case Direction.EAST:
                    if self.east_neighbor().can_move(direction, self.chr):
                        return True
                case Direction.WEST:
                    if self.west_neighbor().can_move(direction, self.chr):
                        return True
                case Direction.NORTH:
                    nn = self.north_neighbor()
                    ob = self.west_neighbor()
                    if barrel_call:
                        return nn.can_move(direction,self.chr)
                    else:
                        return nn.can_move(direction, self.chr) and ob.can_move(direction, self.chr, True)
                case Direction.SOUTH:
                    sn = self.south_neighbor()
                    ob = self.west_neighbor()
                    if barrel_call:
                        return sn.can_move(direction,self.chr)
                    else:
                        return sn.can_move(direction, self.chr) and ob.can_move(direction, self.chr, True)

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
        robot_loc = (match.start()*2, idx)

for y, line in enumerate(map):
    for x, chr in enumerate(line):
        if chr == "O":
            all_cells[(2*x,y)] = Cell((2*x, y), "[")
            all_cells[(2*x+1,y)] = Cell((2*x+1,y), "]")            
        else:
            all_cells[(2*x,y)] = Cell((2*x, y), chr)
            all_cells[(2*x+1,y)] = Cell((2*x+1,y), chr)

print(all_cells)
print("----------------------------")
draw_grid()

for command in commands:
    sleep(.2)
    curr_cell = all_cells[robot_loc]
    print(robot_loc, ":", command)
    match command:
        case "<":
            if curr_cell.west_neighbor().can_move(Direction.WEST, curr_cell.chr):
                robot_loc = (robot_loc[0] - 1, robot_loc[1])
                curr_cell.chr = "."
                curr_cell.west_neighbor().move(Direction.WEST, curr_cell.chr)
            else:
                pass
        case ">":
            if curr_cell.east_neighbor().can_move(Direction.EAST, curr_cell.chr):
                robot_loc = (robot_loc[0] + 1, robot_loc[1])
                curr_cell.chr = "."
                curr_cell.east_neighbor().move(Direction.EAST, curr_cell.chr)
            else:  
                pass    
        case "^":
            if curr_cell.north_neighbor().can_move(Direction.NORTH, curr_cell.chr):
                robot_loc = (robot_loc[0], robot_loc[1] - 1)
                curr_cell.chr = "."
                curr_cell.north_neighbor().move(Direction.NORTH, curr_cell.chr)
            else:  
                pass    
        case "v":
            if curr_cell.south_neighbor().can_move(Direction.SOUTH, curr_cell.chr):
                robot_loc = (robot_loc[0], robot_loc[1] + 1)
                curr_cell.chr = "."
                curr_cell.south_neighbor().move(Direction.SOUTH, curr_cell.chr)
            else:  
                pass
    draw_grid()


total = 0

for y in range(0, max_y):
    for x in range(0, max_x):
        cell = all_cells[(x, y)]
        if cell.chr == "O":
            total += y * 100 + x

print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="b", day=15, year=2024)
