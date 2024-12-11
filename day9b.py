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

# data = sample


disk = []
free_blocks = []
free_chunks = []
used_blocks = []
file_chunks = []
block_counter = 0

for idx, chr in enumerate(data):
    val = int(chr)
    if idx % 2 == 0:
        # This is a file
        file_chunks.append((block_counter, val))
        for i in range(0, val):
            used_blocks.append(block_counter)
            block_counter += 1
            disk.append((idx//2, val))
    else:
        # This is free blocks
        free_chunks.append((block_counter, val))
        for i in range(0, val):
            free_blocks.append(block_counter)
            block_counter += 1      
            disk.append((-1, -1))

print("disk is: ", disk)
print("free blocks are: ", free_blocks)
print("free chunks are: ", free_chunks)
print("used blocks are: ", used_blocks)
print("file chunks are: ", file_chunks)

# Now compact 'em

num_to_move = len(file_chunks)

for i in range(0, num_to_move):
    file_tup = file_chunks.pop()
    src_loc = file_tup[0]
    src_len = file_tup[1]
    src_val = disk[src_loc]
    # print("Finding home for: ", src_val, " with len: ", src_len)
    # print(free_chunks)
    for idx, dest_tup in enumerate(free_chunks[:]):
        dest_avail_len = dest_tup[1]
        dest_start_loc = dest_tup[0]
        # print(dest_avail_len, "-", src_len, "-", dest_start_loc, "-", src_loc)
        if dest_avail_len >= src_len and dest_start_loc < src_loc:
            # now we can move it
            # dest_loc = dest_start_loc
            # print("Moving file no: ", src_val, " to: ", dest_start_loc)
            for i in range(0, src_len):
                disk[dest_start_loc + i] = src_val #write the new file
                disk[src_loc + i] = (-1, -1)
                # print(dest_tup)
            free_chunks.remove(dest_tup)
            # print("checking: ", dest_avail_len, ">", src_len)
            if dest_avail_len > src_len:
                # print("Creating new free chunk: ", (dest_start_loc + src_len, dest_tup[1] - src_len))
                free_chunks.insert(idx, ((dest_tup[0] + src_len), (dest_tup[1] - src_len)))
            break

print("disk is: ", disk)
# print("free blocks are: ", free_blocks)
# print("free chunks are: ", free_chunks)
# print("used blocks are: ", used_blocks)
# print("file chunks are: ", file_chunks)

total = 0

for idx, val in enumerate(disk):
    if val[0] > -1:
        # print("total +=", val[0], "*", idx)
        total += val[0] * idx


print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="b", day=9, year=2024)