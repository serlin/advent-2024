import string
import re
import copy
import functools
import itertools
from functools import cmp_to_key
import networkx as nx
from enum import Enum
import aocd
from time import sleep

data = aocd.get_data(day=16, year=2024)

sample = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

sample2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

# data = sample

map = data.splitlines()
robot_loc = (-1, -1)
start_loc = (-1, -1)
end_loc = (-1, -1)

all_cells = {} #((x,y), dir), Cell
print(map)

max_x = len(map[0])
max_y = len(map)

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

all_dirs = {Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST}


class Cell:
    global all_cells
    global max_x
    global max_y
    def __init__(self, location, chr, facing):
        self.chr = chr
        if chr == "S" or chr == "E":
            self.chr = "."
        self.location = location
        self.facing = facing

    def __str__(self):
        return f'{self.location}: {self.chr}: {self.facing}'
    
    def __repr__(self):
        return f'{self.location}: {self.chr}: {self.facing}'
    
    def east_neighbor(self):
        new_loc = ((self.location[0]+1, self.location[1]), Direction.EAST)
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None
        
    def west_neighbor(self):
        new_loc = ((self.location[0]-1, self.location[1]), Direction.WEST)
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None

    def north_neighbor(self):
        new_loc = ((self.location[0], self.location[1]-1), Direction.NORTH)
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None

    def south_neighbor(self):
        new_loc = ((self.location[0], self.location[1]+1), Direction.SOUTH)
        if new_loc in all_cells:
            return all_cells[new_loc]
        else:
            return None
    
    def connected_rotations(self):
        ret = []
        other_dirs = all_dirs - {self.facing}
        for dir in other_dirs:
            ret.append(all_cells[(self.location, dir)])
        return ret

    def connected_cell_in_line(self):
        ret = []
        if self.chr == "#":
            # I'm a wall, I connect to nothing
            return []
        if self.facing == Direction.EAST:
            if self.east_neighbor() and self.east_neighbor().chr == ".":
                ret.append(self.east_neighbor())
        if self.facing == Direction.WEST:
            if self.west_neighbor() and self.west_neighbor().chr == ".":
                ret.append(self.west_neighbor())
        if self.facing == Direction.SOUTH:
            if self.south_neighbor() and self.south_neighbor().chr == ".":
                ret.append(self.south_neighbor())
        if self.facing == Direction.NORTH:
            if self.north_neighbor() and self.north_neighbor().chr == ".":
                ret.append(self.north_neighbor())
        return ret

def draw_grid():
    print("----------------------------------------------------------------------------------")
    for y in range(0, max_y):
        print("")
        for x in range(0, max_x):
            if (x,y) == robot_loc:
                print("R", end='')
            else: 
                print(all_cells[((x, y), Direction.NORTH)].chr, end='')
    print("\n----------------------------------------------------------------------------------")


for idx, line in enumerate(map):
    match = re.search("S", line)
    if match:
        print("found start at: ", match.start(), ":", idx)
        start_loc = (match.start(), idx)
    match = re.search("E", line)
    if match:
        print("found end at:: ", match.start(), ":", idx)
        end_loc = (match.start(), idx)

for y, line in enumerate(map):
    for x, chr in enumerate(line):
            for dir in all_dirs:
                all_cells[((x,y), dir)] = Cell((x, y), chr, dir)

start_cell = all_cells[(start_loc, Direction.EAST)]
end_cells = [all_cells[(end_loc, Direction.NORTH)], all_cells[(end_loc, Direction.SOUTH)], all_cells[(end_loc, Direction.WEST)], all_cells[(end_loc, Direction.EAST)]]

print(all_cells)
print("----------------------------")
draw_grid()

G = nx.DiGraph()

# G.add_nodes_from(all_cells)
print(G)

for loc, cell in all_cells.items():
    # print("Adding heavy weight turns")
    for tar in cell.connected_rotations():
        # print (cell, "->", tar, ": 1000")
        G.add_edge(cell, tar, weight=1000)
    
    for tar in cell.connected_cell_in_line():
        # print (cell, "->", tar, ": 1")
        G.add_edge(cell, tar, weight=1)

print(G)

paths = [nx.shortest_path_length(G, source=start_cell, target=end_cell, weight="weight") for end_cell in end_cells]
print(paths)

total = min(paths)
print ("Total is: ", total, "submitting...")

seats = set()

for end_cell in end_cells:
    for path in nx.all_shortest_paths(G, source=start_cell, target=end_cell, weight="weight"):
        if nx.path_weight(G, path, weight="weight") == total:
            for cell in path:
                seats.add(cell)

unique_locs = set()
for dir_cell in seats:
    unique_locs.add(dir_cell.location)

print(len(seats))
print(len(unique_locs))
# aocd.submit(total, part="b", day=15, year=2024)
