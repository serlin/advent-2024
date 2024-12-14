import string
import re
import copy
import functools
import itertools
from functools import cache
from operator import mul
from operator import add
from enum import Enum
import numpy as np
import aocd
from math import isclose

data = aocd.get_data(day=13, year=2024)

sample = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

lines = data.splitlines()
buttons_a = []
buttons_b = []
prize_locs = []

a_cost = 3
b_cost = 1

for line in lines:
    nums = re.findall("\\d+", line)
    if line.startswith("Button A:"):
        buttons_a.append((int(nums[0]), int(nums[1])))
    elif line.startswith("Button B:"):
        buttons_b.append((int(nums[0]), int(nums[1])))
    elif line.startswith("Prize:"):
        prize_locs.append((int(nums[0]), int(nums[1])))

def is_whole(num):
    return isclose(num/round(num), 1)

total = 0
for idx, loc in enumerate(prize_locs):
    a = buttons_a[idx]
    b = buttons_b[idx]

    arr1 = np.array([[a[0], b[0]], [a[1], b[1]]])
    arr2 = np.array([loc[0], loc[1]])
    answers = np.linalg.solve(arr1, arr2)
    
    cost = 0
    if is_whole(answers[0]) and is_whole(answers[1]) and answers[0] > -1 and answers[1] > -1 and answers[0] < 100 and answers[1] < 100:
        cost = int(round(answers[0])) * 3 + int(round(answers[1]))
    
    print("Adding cost of: ", cost)
    total += cost

print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="a", day=13, year=2024)
