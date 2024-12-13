import string
import re
import copy
import functools
import itertools
import aocd
from enum import Enum

data = aocd.get_data(day=12, year=2024)

sample = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""" 

sample2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

sample3 = """AAAA
BBCD
BBCC
EEEC
"""

sample4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

sample5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""


# data = sample

lines = data.splitlines()

max_x = len(lines[0])
max_y = len(lines)

all_cells = {} # (x, y), chr
all_fences = {} # chr, [fence_count]
all_regions = {} # chr, set of cells
walked = set()

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
        self.plant = chr
        self.location = location
        self.neighbors = set() # Cell
        self.counted_fence_directions = set()
        self.counted_fences = False

    def __str__(self):
        return f'{self.location}: {self.plant}'
    
    def __repr__(self):
        return f'{self.location}: {self.plant}'
    
    def same_plant_neighbors(self):
        ret = set()
        for neighbor in self.neighbors:
            if neighbor.plant == self.plant:
                ret.add(neighbor)
        return ret
    
    def diff_plant_neighbors(self):
        ret = set()
        for neighbor in self.neighbors:
            if neighbor.plant != self.plant:
                ret.add(neighbor)
        return ret

    def num_fences(self):
        return 4 - len(self.same_plant_neighbors())
    
    def fence_dirs(self):
        ret = []
        for neighbor in self.diff_plant_neighbors():
            # print(neighbor)
            if neighbor.location[0] > self.location[0]:
                ret.append(Direction.EAST)
            elif neighbor.location[0] < self.location[0]:
                ret.append(Direction.WEST)
            elif neighbor.location[1] < self.location[1]:
                ret.append(Direction.NORTH)
            elif neighbor.location[1] > self.location[1]:
                ret.append(Direction.SOUTH)
            else:
                print("WTAF?")
        if self.location[0] == 0:
            ret.append(Direction.WEST)
        if self.location[1] == 0:
            ret.append(Direction.NORTH)
        if self.location[0] == max_x - 1:
            ret.append(Direction.EAST)
        if self.location[1] == max_y - 1:
            ret.append(Direction.SOUTH)
        return ret

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



def walk(next_cell):
    # print("walking from: ", next_cell)
    # if this call can walk to no other cells that aren't already in the region with the same letter
    global walked
    walkable_neighbors = next_cell.same_plant_neighbors() - walked
    res = []
    walked.add(next_cell)
    if walkable_neighbors:
        # for each walkable neighbor
        res.append(next_cell)
        for neighbor in walkable_neighbors:
            # print("Walking to neighbor: ", neighbor)
            # print("walked:", walked)
            res.extend(walk(neighbor))
        return res
    else:
        # print("ran out of neighbors")
        return [next_cell]


for y, line in enumerate(lines):
    for x, chr in enumerate(line):
        all_cells[(x, y)] = Cell((x, y), chr)

for cell in all_cells.values():
    loc = cell.location

    if loc[0] > 0:
        cell.neighbors.add(all_cells[((loc[0] - 1), loc[1])])
    if loc[0] < len(lines[0]) - 1:
        cell.neighbors.add(all_cells[((loc[0] + 1), loc[1])])
    if loc[1] > 0:
        cell.neighbors.add(all_cells[((loc[0]), loc[1] - 1)])
    if loc[1] < len(lines) - 1:
        cell.neighbors.add(all_cells[((loc[0]), loc[1] + 1)])

for cell in all_cells.values():
    if cell.plant not in all_fences:
        all_fences[cell.plant] = []
    all_fences[cell.plant].append(cell.num_fences())

all_locs = all_cells.keys()

for i, loc in enumerate(all_locs):
    if all_cells[loc] not in walked:   
        all_regions[f'{all_cells[loc].plant}{i}'] = set(walk(all_cells[loc]))


# print("Regions: ")
# print(all_regions)

total = 0
for key, arr in all_regions.items():
    fences = 0
    for cell in arr:
        fences += cell.num_fences()
    # print("Region:", key, "Number fences: ", fences, "Number plots, ", len(arr))
    total += fences * len(arr)

print("Part 1 total: ", total)

total = 0

print(all_regions)

for key, arr in all_regions.items():
    print("Doing region: ", key)
    sides = 0
    for cell in sorted(arr, key=lambda c: c.location):
        # cell.counted_fences = 
        print(cell)
        fence_dirs = cell.fence_dirs()
        print("fences in: ", fence_dirs)
        neighbors_to_update = cell.same_plant_neighbors()
        loc = cell.location
        for dir in fence_dirs:
            if dir not in cell.counted_fence_directions:
                # total += 1
                print("Adding side: ", dir, " for: ", cell)
                sides += 1
                cell.counted_fence_directions.add(dir)
            match dir:
                case Direction.NORTH:
                    if cell.east_neighbor() in neighbors_to_update:
                        cell.east_neighbor().counted_fence_directions.add(Direction.NORTH)
                    if cell.west_neighbor() in neighbors_to_update:
                        cell.west_neighbor().counted_fence_directions.add(Direction.NORTH)                                                              
                case Direction.EAST:
                    if cell.north_neighbor() in neighbors_to_update:
                        cell.north_neighbor().counted_fence_directions.add(Direction.EAST)
                    if cell.south_neighbor() in neighbors_to_update:
                        cell.south_neighbor().counted_fence_directions.add(Direction.EAST)
                case Direction.SOUTH:
                    if cell.east_neighbor() in neighbors_to_update:
                        cell.east_neighbor().counted_fence_directions.add(Direction.SOUTH)
                    if cell.west_neighbor() in neighbors_to_update:
                        cell.west_neighbor().counted_fence_directions.add(Direction.SOUTH)                                                              
                case Direction.WEST:
                    if cell.north_neighbor() in neighbors_to_update:
                        cell.north_neighbor().counted_fence_directions.add(Direction.WEST)
                    if cell.south_neighbor() in neighbors_to_update:
                        cell.south_neighbor().counted_fence_directions.add(Direction.WEST)
    print("Listing found fences")
    for cell in arr:
        print(cell, ": ", cell.counted_fence_directions)
    print("Total sides in region: ", sides)
    total += len(arr) * sides
    print("Cost of region: ", len(arr) * sides)
  
# for each cell in a region add nonneighbor directions

print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="b", day=12, year=2024)