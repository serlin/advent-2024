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
# lines = data.splitlines()

@cache
def update_stone(stone):
    n = len(stone)
    if stone == "0":
        return ["1"]
    elif n % 2 == 0:
        l = stone[:n//2]
        r = stone[n//2:].lstrip("0")
        if r == "":
            r = "0"
        return [l, r]
    else:
        return [str(int(stone) * 2024)]

for i in range(0, 25):
# Each blink
    print("Blink: ", i)
    old_stones = stones.copy()
    stones = []
    for stone in old_stones:
        stones.extend(update_stone(stone))
    # print(stones)

total = len(stones)
print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=11, year=2024)
