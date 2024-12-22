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

    def cheats(self):
        ret = [] # ((x, y), (x, y))
        if self.chr == ".":
            return []
        else:
            # if I'm a wall and I have 2 non-wall neighbors then I'm a single cheat.
            if len(self.non_wall_neighbors()) >= 2:
                ret.append((self.location, self.location))
            for neighbor in self.wall_neighbors():
                if len(self.non_wall_neighbors()) > 0 and len(neighbor.non_wall_neighbors()) > 0:
                    if self.location > neighbor.location:
                        ret.append((self.location, neighbor.location))
                    else:
                        ret.append((neighbor.location, self.location))
            return ret
            # also if I have at least 1 non-wall neighbour and one of my wall neighbours has a different non-wall neighbour, that's a double cheat.

def draw_grid():
    print("----------------------------------------------------------------------------------")
    for y in range(0, max_y):
        print("")
        for x in range(0, max_x):
            print(all_cells[(x, y)].chr, end='')
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
            all_cells[(x,y)] = Cell((x, y), chr)

start_cell = all_cells[(start_loc)]
end_cell = all_cells[(end_loc)]

# print(all_cells)
print("----------------------------")
draw_grid()

G = nx.DiGraph()
print(G)

for loc, cell in all_cells.items():
    if cell.chr == ".":
        for tar in cell.non_wall_neighbors():
            G.add_edge(cell, tar)
            G.add_edge(tar, cell)

full_run = nx.shortest_path_length(G, source=start_cell, target=end_cell)
print("Full run: ", full_run)
print(G)

all_cheats = set()

# create a set of cheats ((x1,y1), (x2,y2)) or ((x1,y1), (x1, y1))

for y in range(1, max_y - 1):
    for x in range(1, max_x -1):
        cell = all_cells[(x,y)]
        cheat_set = set(cell.cheats())
        # print("Cell:", cell, " cheats: ", cheat_set)
        all_cheats.update(cheat_set)

print("All cheats are: ", all_cheats)

new_lengths = []

for cheat in all_cheats:

    if cheat[0] == cheat[1]:
        # single point cheat
        cell = all_cells[cheat[0]]

        for n in cell.non_wall_neighbors():
            # print("Adding edge between: ", cell, "->", n)
            G.add_edge(n, cell)
            G.add_edge(cell, n)
        
        new_lengths.append(nx.shortest_path_length(G, source=start_cell, target=end_cell))
        for n in cell.non_wall_neighbors():
            G.remove_edge(cell, n)
            G.remove_edge(n, cell)
        # two point cheat
    else:
        cell1 = all_cells[cheat[0]]
        cell2 = all_cells[cheat[1]]
        G.add_edge(cell1, cell2)
        for n in cell1.non_wall_neighbors():
            # print("Adding edge between: ", cell1, "->", n)
            G.add_edge(cell1, n)
            G.add_edge(n, cell1)
        for n in cell2.non_wall_neighbors():
            # print("Adding edge between: ", cell2, "->", n)
            G.add_edge(cell2, n)
            G.add_edge(n, cell2)
            

        new_lengths.append(nx.shortest_path_length(G, source=start_cell, target=end_cell))

        for n in cell1.non_wall_neighbors():
            G.remove_edge(cell1, n)
            G.remove_edge(n, cell1)
        for n in cell2.non_wall_neighbors():
            G.remove_edge(cell2, n)
            G.remove_edge(n, cell2)

        G.remove_edge(cell1, cell2)
        
# d = {}
# for l in new_lengths:
#     diff = full_run - l
#     if diff not in d.keys():
#         d[diff] = 0
#     d[diff] += 1

total = 0
for l in new_lengths:
    diff = full_run - l
    if diff > 0:
        print(diff)
    if diff >= 100:
        total += 1

print("total cheats: ", len(all_cheats))

print(total)
# for each cheat
# add edges between (x1, y1) and all its non_wall_neighbors
# do the same thing for (x2, y2) (if it exists)

# measure the shortest route again and figure out how much time was saved

# repeat?



# paths = [nx.shortest_path_length(G, source=start_cell, target=end_cell, weight="weight") for end_cell in end_cells]
# print(paths)

# total = min(paths)
# print ("Total is: ", total, "submitting...")

# seats = set()

# for end_cell in end_cells:
#     for path in nx.all_shortest_paths(G, source=start_cell, target=end_cell, weight="weight"):
#         if nx.path_weight(G, path, weight="weight") == total:
#             for cell in path:
#                 seats.add(cell)

# unique_locs = set()
# for dir_cell in seats:
#     unique_locs.add(dir_cell.location)

# print(len(seats))
# print(len(unique_locs))
# aocd.submit(total, part="b", day=15, year=2024)
