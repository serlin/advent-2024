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
from time import sleep

data = aocd.get_data(day=14, year=2024)

sample = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

# data = sample
# map_width = 11
# map_height = 7
# quad_x = 4 # 0 .. n n+2 .. width - 1
# quad_y = 2 

map_width = 101
map_height = 103
quad_x = 49
quad_y = 50

lines = data.splitlines()

class Robot:
    def __init__(self, location, velocity):
        self.location = location #(x, y)
        self.velocity = velocity #(x, y)

    def __str__(self):
        return f'|p{self.location}: v{self.velocity}|'
    
    def __repr__(self):
        return f'|{self.location}: v{self.velocity}|'

robots = [] #[Robot]

for line in lines:
    print(line)
    nums = re.findall("-?\\d+,-?\\d+", line)
    print(nums)

    loc = nums[0].strip().split(",")
    vel = nums[1].strip().split(",")
    robots.append(Robot((int(loc[0]), int(loc[1])), (int(vel[0]), int(vel[1]))))    

# print(robots)

def move_with_wrap(num):
    for robot in robots:
        mv_x = (robot.velocity[0] * num) % (map_width)
        mv_y = (robot.velocity[1] * num) % (map_height)

        new_x = (robot.location[0] + mv_x) % (map_width)
        new_y = (robot.location[1] + mv_y) % (map_height)

        robot.location = ((new_x, new_y))

def make_grid():
    grid = []
    s = "." * map_width
    for y in range(0, map_height):
        grid.append(s)
    
    for robot in robots:
        x = robot.location[0] 
        y = robot.location[1]
        grid[y] = grid[y][:x] + "X" + grid[y][x+1:]
    
    return grid


# move_with_wrap(100)
# print("----------------------------")
# print(robots)



# # count quadrants
# quads = [0,0,0,0] # UL, UR, LL, LR

# for robot in robots:
#     loc = robot.location
#     if loc[0] <= quad_x:
#         if loc[1] <= quad_y:
#             quads[0] += 1  
#         elif loc[1] >= quad_y + 2:
#             quads[2] += 1
#         else:
#             pass 
#     elif loc[0] >= quad_x + 2:
#         if loc[1] <= quad_y:
#             quads[1] += 1  
#         elif loc[1] >= quad_y + 2:
#             quads[3] += 1
#         else:
#             pass
#     else:
#         pass #It's on the x line


# print(quads)

# # move_with_wrap(1)
# # print("----------------------------")
# # print(robots)


# total = 1
# for quad in quads:
#     total = total * quad

for i in range(0, 15000):
    move_with_wrap(1)
    print("----------------------------------------------")
    print("Second: ", i)
    grid = make_grid()
    for s in grid:
        print(s)
    # sleep(0.2)

total = 0
print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="b", day=13, year=2024)
