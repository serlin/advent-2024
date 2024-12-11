import string
import re
import copy
import functools
import itertools
import bisect
from operator import mul
from operator import add
from enum import Enum
import aocd
from numpy import tile

data = aocd.get_data(day=9, year=2024)

sample = "2333133121414131402"

data = sample


disk = []
free_blocks = []
used_blocks = []
block_counter = 0

for idx, chr in enumerate(data):
    val = int(chr)
    if idx % 2 == 0:
        # This is a file
        for i in range(0, val):
            used_blocks.append(block_counter)
            block_counter += 1
            disk.append(idx//2)
    else:
        # This is free blocks
        for i in range(0, val):
            free_blocks.append(block_counter)
            block_counter += 1      
            disk.append(-1)

print("disk is: ", disk)
print("free blocks are: ", free_blocks)
print("used blocks are: ", used_blocks)


# Now compact 'em

num_to_move = len(free_blocks)

for i in range(0, num_to_move):
    src_loc = used_blocks.pop()
    src_val = disk[src_loc]
    disk[src_loc] = -1
    dest_loc = free_blocks.pop(0)
    disk[dest_loc] = src_val
    bisect.insort(free_blocks, src_loc)
    bisect.insort(used_blocks, dest_loc)
    # tilele dest = free_blocks.pop(0):
    # dest = free_blocks.pop(0)
    # # dest = block
    # src = used_blocks.pop()
    # disk[dest] = disk[src]
    # disk[src] = -1

print("disk is: ", disk)
print("free blocks are: ", free_blocks)
print("used blocks are: ", used_blocks)


total = 0

for idx, val in enumerate(used_blocks):
    total += disk[val] * idx


print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="b", day=9, year=2024)