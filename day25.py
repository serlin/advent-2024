import string
import re
import copy
import functools
import itertools
from functools import cmp_to_key
from functools import cache
import networkx as nx
from enum import Enum
import aocd
from time import sleep

data = aocd.get_data(day=25, year=2024)

sample = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

# data = sample

things = data.split("\n\n")

keys = [] # [[x,x,x,x,x]]
locks = [] # [[y,y,y,y,y]]

for thing in things:
    if thing.splitlines()[0] == ".....":
        key = [-1,-1,-1,-1,-1]
        for line in thing.splitlines():
            # key    
            for idx, chr in enumerate(line):
                if chr == "#":
                    key[idx] += 1
        keys.append(key)
    else:
        lock = [-1,-1,-1,-1,-1]
        for line in thing.splitlines():
            #lock
            for idx, chr in enumerate(line):
                if chr == "#":
                    lock[idx] += 1
        locks.append(lock)

total = 0

for key, lock in itertools.product(keys, locks):
    works = True

    print("Checking: ", key, lock)
    for idx in range(0,5):
        if key[idx] + lock[idx] >= 6:
            print("It didn't work")
            works = False
            break
        else:
            pass
    if works:
        print("It worked")
        total += 1

print("keys:", keys)
print("locks:", locks)

print(total)
# aocd.submit(total, part="b", day=18, year=2024)
