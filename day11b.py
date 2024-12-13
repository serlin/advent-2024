import string
import re
import copy
import functools
import itertools
from functools import cache
from operator import mul
from operator import add
from enum import Enum
import aocd

data = aocd.get_data(day=11, year=2024)

sample = "125 17"

# data = sample

stones = data.split(" ")
stones = [int(x) for x in stones]

@cache
def update_stone(stone, times):
    if times == 75:
        return 1
    
    s = str(stone)
    n = len(str(stone))

    # print("stone: ", stone)
    next_stones = []
    if stone == 0:
        next_stones = [1]
    elif n % 2 == 0:
        l = s[:n//2]
        r = s[n//2:].lstrip("0")
        if r == "":
            r = "0"
        next_stones = [int(l), int(r)]
    else:
       next_stones = [stone * 2024]
    return sum(update_stone(stone, times + 1) for stone in next_stones) #if update_stone(stone, times + 1) != -1)


old_stones = stones.copy()
stones = []

# for stone in old_stones:
total = sum(update_stone(stone, 0) for stone in old_stones)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=11, year=2024)
