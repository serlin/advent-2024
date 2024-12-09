import string
import re
import copy
import functools
import itertools
from operator import mul
from operator import add
from enum import Enum
import aocd

data = aocd.get_data(day=7, year=2024)

sample = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

# data = sample

def elecat(x, y):
    return int(f"{x}{y}")

all_funcs = [mul, add, elecat]

lines = data.splitlines()
results = []
values = []

def do_math(num_arr, func_arr):
    # print("doing math:", num_arr, func_arr)
    total = num_arr[0]
    for idx, func in enumerate(func_arr):
        # print("func is: ", func)
        total = func(total, num_arr[idx + 1])
    return total

for line in lines:
    colon = line.split(":")
    results.append(int(colon[0]))
    arr = colon[1].strip().split(" ")
    arr = [int(x) for x in arr]
    values.append(arr)

total = 0

for idx, result in enumerate(results):
    if len(values[idx]) > 2:
        # funcs = itertools.combinations_with_replacement(all_funcs, len(values[idx]) - 1)
        # funcs = itertools.permutations(all_funcs, len(values[idx]) - 1)
        funcs = itertools.product(all_funcs, repeat=len(values[idx]) - 1)
    else: 
        funcs = [[mul], [add]]
    # print("all funcs are", list(funcs))
    for fn_arr in funcs:
        if result == do_math(values[idx], fn_arr):
            # print("Good math: ", values[idx], " --- ", fn_arr, " ---- Total: ", result)
            total += result
            break


print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=7, year=2024)