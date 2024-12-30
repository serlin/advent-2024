import string
import re
import copy
import functools
import itertools
from functools import cache
import networkx as nx
from enum import Enum
import aocd
from time import sleep
# from numpy import bitwise_xor

data = aocd.get_data(day=22, year=2024)

sample = """1
2
3
2024"""

# data = sample
seeds = data.splitlines()

def prune(num):
    return num % 16777216

def mix(num, mixer):
    return num ^ mixer

@cache
def next_secret(current_secret):
    n = current_secret * 64
    n = mix(current_secret, n)
    n = prune(n)
    m = n // 32
    n = mix(n, m)
    n = prune(n)
    m = n * 2048
    n = mix(n, m)
    n = prune(n)
    return n

total = 0
seq_dict = {} # (1,2,3,4), [vals]
holder_arr = []
last_mod = 0
for line in seeds:
    holder_arr = []
    num = int(line)
    last_mod = num % 10
    # holder_arr.append(last_mod)

    for i in range(0, 2000):
        num = next_secret(num)
        holder_arr.append(((num % 10) - last_mod, (num % 10)))
        last_mod = num % 10

    local_check = set()
    for idx in range(0, len(holder_arr) - 3):
        tup = (holder_arr[idx][0], holder_arr[idx+1][0], holder_arr[idx+2][0], holder_arr[idx+3][0])
        if tup in local_check:
            next
        else:
            local_check.add(tup)
            # print(tup)
            if tup in seq_dict:
                # print("Adding: ", holder_arr[idx+3][1], " to: ", tup)
                # print(seq_dict[tup])
                seq_dict[tup].append(holder_arr[idx+3][1])
            else:
                # print("Creating: ", holder_arr[idx+3][1], " for: ", tup)
                seq_dict[tup] = [holder_arr[idx+3][1]]

# print("Res:", seq_dict[(-2,1,-1,3)])

max_val = 0
max_tup = ()
for key, val in seq_dict.items():
    tot = sum(val)
    if tot > max_val:
        max_val = tot
        max_tup = key
    # print(line, ": ", num)
    # total += num

print("Big one:", max_tup, ": ", max_val)
print("Part 1 totaL: ", total)


