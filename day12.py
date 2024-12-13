import string
import re
import copy
import functools
import itertools
import aocd

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


# data = sample2

lines = data.splitlines()

all_cells = {} # (x, y), chr
all_fences = {} # chr, [fence_count]
all_regions = {} # chr, [(x, y)]
walked = set()

class Cell:
    def __init__(self, location, chr):
        self.plant = chr
        self.location = location
        self.neighbors = set() # Cell

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
    
    def num_fences(self):
        return 4 - len(self.same_plant_neighbors())

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


print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="a", day=12, year=2024)
# counter is answer for part 