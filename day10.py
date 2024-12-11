import string
import re
import copy
import functools
import itertools
from operator import mul
from operator import add
from enum import Enum
import aocd

data = aocd.get_data(day=10, year=2024)

sample = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

# data = sample

lines = data.splitlines()

all_cells = {}
counter = 0
peaks_per_head = set()

class Cell:

    def __init__(self, el, location):
        self.elevation = el
        self.location = location
        self.neighbors = []

    def __str__(self):
        return f'{self.location}, ele: {self.elevation}'
    
    def __repr__(self):
        return f'{self.location}, ele: {self.elevation}'
    
    def walkable_neighbors(self):
        ret = []
        for neighbor in self.neighbors:
            if neighbor.elevation == self.elevation + 1:
                ret.append(neighbor)
        return ret        


def walk(next_cell, head):
    # if this one's elevation is 9 then add to the counter and return (or just return true)
    global counter
    # print("walking from: ", next_cell, head)
    if next_cell.elevation == 9:
        # print("found peak at:", next_cell)
        peaks_per_head.add((next_cell, head))
        counter += 1
        return True
    else:
        for neighbor in next_cell.walkable_neighbors():
            # print("walking to: ", neighbor)
            walk(neighbor, cell)
    # Otherwise grab any walkable cells and recurse


for y, line in enumerate(lines):
    for x, chr in enumerate(line):
        all_cells[(x, y)] = Cell(int(chr), (x, y))


# print(all_cells.keys())

for cell in all_cells.values():
    # populate neighbors
    loc = cell.location

    if loc[0] > 0:
        cell.neighbors.append(all_cells[((loc[0] - 1), loc[1])])
    if loc[0] < len(lines[0]) - 1:
        cell.neighbors.append(all_cells[((loc[0] + 1), loc[1])])
    if loc[1] > 0:
        cell.neighbors.append(all_cells[((loc[0]), loc[1] - 1)])
    if loc[1] < len(lines) - 1:
        cell.neighbors.append(all_cells[((loc[0]), loc[1] + 1)])

for cell in all_cells.values():
    if cell.elevation == 0:
        walk(cell, cell)

print("peaks per head: ", len(peaks_per_head))
print("counter: ", counter)

total = len(peaks_per_head)
print ("Total is: ", total, "submitting...")
aocd.submit(total, part="a", day=10, year=2024)
# counter is answer for part b