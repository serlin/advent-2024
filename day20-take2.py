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

data = aocd.get_data(day=20, year=2024)

sample = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


# data = sample

map = data.splitlines()
start_loc = (-1, -1)
end_loc = (-1, -1)

all_cells = {} #(x,y), Cell
print(map)

max_x = len(map[0])
max_y = len(map)

class Cell:
    global all_cells
    global max_x
    global max_y

    end_dist = -1
    def __init__(self, location, chr):
        self.chr = chr
        if chr == "S" or chr == "E":
            self.chr = "."
        self.location = location

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
    
    def neighbors(self):
        return [x for x in [self.east_neighbor(), self.west_neighbor(), self.north_neighbor(), self.south_neighbor()] if x]

    def non_wall_neighbors(self):
        ret = []
        for neighbor in self.neighbors():
            if neighbor.chr == ".":
                ret.append(neighbor)
        return ret

    def wall_neighbors(self):
        ret = []
        for neighbor in self.neighbors():
            if neighbor.chr == "#":
                ret.append(neighbor)
        return ret

def draw_grid():
    print("----------------------------------------------------------------------------------")
    for y in range(0, max_y):
        print("")
        for x in range(0, max_x):
            print(all_cells[(x, y)].chr, end='')
    print("\n----------------------------------------------------------------------------------")

def cell_distance(c1, c2):
    return abs(c1.location[0] - c2.location[0]) + abs(c1.location[1] - c2.location[1])


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
            all_cells[(x,y)] = Cell((x, y), chr)

start_cell = all_cells[(start_loc)]
end_cell = all_cells[(end_loc)]

# print(all_cells)
print("----------------------------")
draw_grid()

G = nx.Graph()
print(G)

for loc, cell in all_cells.items():
    if cell.chr == ".":
        for tar in cell.non_wall_neighbors():
            G.add_edge(cell, tar)

full_run_length = nx.shortest_path_length(G, source=start_cell, target=end_cell)
full_run = nx.shortest_path(G, source=start_cell, target=end_cell)

for idx, cell in enumerate(full_run):
    # print(idx, ": ", cell)
    cell.end_dist = full_run_length - idx

print("Full run length: ", full_run_length)
# print(G)
total = 0

for (c1, c2) in itertools.combinations(full_run, 2):
    distance = cell_distance(c1, c2)
    if distance <= 2:
        if abs(c1.end_dist - c2.end_dist) - distance >= 100:
            total +=1

print("Part 1 totaL: ", total)

total = 0

for (c1, c2) in itertools.combinations(full_run, 2):
    distance = cell_distance(c1, c2)
    if distance <= 20:
        if abs(c1.end_dist - c2.end_dist) - distance >= 100:
            total +=1

print("Part 2 totaL: ", total)

