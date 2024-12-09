import string
import re
import copy
import functools
import itertools
from operator import mul
from operator import add
from enum import Enum
import aocd

data = aocd.get_data(day=8, year=2024)

sample = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

# data = sample

def elecat(x, y):
    return int(f"{x}{y}")

all_funcs = [mul, add, elecat]

lines = data.splitlines()

antenna_dict = {} # chr: [(x, y)]
nodal_dict = {}
nodal_set = set()

for idx, line in enumerate(lines):
    for ant_loc in re.finditer("[^\\.]", line):
        if ant_loc[0] not in antenna_dict:
            antenna_dict[ant_loc[0]] = []
        antenna_dict[ant_loc[0]].append((ant_loc.start(), idx))

print(antenna_dict)

total = 0


for antenna_chr in antenna_dict:
    arr = antenna_dict[antenna_chr]
    if antenna_chr not in nodal_dict:
        nodal_dict[antenna_chr] = set()
    for pair in itertools.combinations(arr, 2):
        print(antenna_chr, "-", pair)
        diff_x = (pair[1][0] - pair[0][0])
        diff_y = (pair[1][1] - pair[0][1])

        x1 = pair[0][0] - diff_x
        x2 = pair[1][0] + diff_x
        y1 = pair[0][1] - diff_y
        y2 = pair[1][1] + diff_y
        if x1 >= 0 and x1 < len(lines[0]) and y1 >= 0 and y1 < len(lines):
            # nodal_dict[antenna_chr].add((x1, y1))
            nodal_set.add((x1, y1))
        if x2 >= 0 and x2 < len(lines[0]) and y2 >= 0 and y2 < len(lines):
            # nodal_dict[antenna_chr].add((x2, y2))
            nodal_set.add((x2, y2))

print(nodal_dict)

# for chr in nodal_set:
#     total += len(nodal_dict[chr])
# total = len(nodal_dict.keys())
total = len(nodal_set)
print ("Total is: ", total, "submitting...")
aocd.submit(total, part="a", day=8, year=2024)