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
10
100
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
for line in seeds:
    num = int(line)
    for i in range(0, 2000):
        num = next_secret(num)
    print(line, ": ", num)
    total += num

print("Part 1 totaL: ", total)


