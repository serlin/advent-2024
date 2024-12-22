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

data = aocd.get_data(day=19, year=2024)

sample = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

# data = sample

parts = data.split("\n\n")[0].strip()
towels = data.split("\n\n")[1].splitlines()

parts = re.findall("\\w+", parts)


print(parts)
print(towels)

@cache
def check(remain):
    print("searching for: ", remain)
    global parts

    ret = False
    if remain == "":
        return True
    for part in parts:
        if remain.startswith(part):
            next_part = remain[len(part):]
            if check(next_part):
                return True
        
    return False

total = 0

for towel in towels:
    # print("Checking: ", towel)
    if check(towel):
        # print("towel: ", towel, "is possible")
        total += 1


print(total)
# aocd.submit(total, part="b", day=18, year=2024)
