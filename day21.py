import string
import re
import copy
import functools
import itertools
from itertools import pairwise
from functools import cache
import networkx as nx
from enum import Enum
import aocd
from time import sleep

data = aocd.get_data(day=21, year=2024)

sample = """029A
980A
179A
456A
379A
"""

# data = sample

codes = data.splitlines()

numpad = nx.DiGraph()
controller = nx.DiGraph()

numpad.add_edge("7", "8", command=">")
numpad.add_edge("8", "9", command=">")
numpad.add_edge("4", "5", command=">")
numpad.add_edge("5", "6", command=">")
numpad.add_edge("1", "2", command=">")
numpad.add_edge("2", "3", command=">")
numpad.add_edge("0", "A", command=">")
numpad.add_edge("9", "8", command="<")
numpad.add_edge("8", "7", command="<")
numpad.add_edge("6", "5", command="<")
numpad.add_edge("5", "4", command="<")
numpad.add_edge("3", "2", command="<")
numpad.add_edge("2", "1", command="<")
numpad.add_edge("A", "0", command="<")
numpad.add_edge("7", "4", command="v")
numpad.add_edge("4", "1", command="v")
numpad.add_edge("8", "5", command="v")
numpad.add_edge("5", "2", command="v")
numpad.add_edge("2", "0", command="v")
numpad.add_edge("9", "6", command="v")
numpad.add_edge("6", "3", command="v")
numpad.add_edge("3", "A", command="v")
numpad.add_edge("1", "4", command="^")
numpad.add_edge("4", "7", command="^")
numpad.add_edge("0", "2", command="^")
numpad.add_edge("2", "5", command="^")
numpad.add_edge("5", "8", command="^")
numpad.add_edge("A", "3", command="^")
numpad.add_edge("3", "6", command="^")
numpad.add_edge("6", "9", command="^")

controller.add_edge("<", "v", command=">")
controller.add_edge("v", "<", command="<")
controller.add_edge("v", "^", command="^")
controller.add_edge("^", "v", command="v")
controller.add_edge("^", "A", command=">")
controller.add_edge("A", "^", command="<")
controller.add_edge("v", ">", command=">")
controller.add_edge(">", "v", command="<")
controller.add_edge(">", "A", command="^")
controller.add_edge("A", ">", command="v")

print("Numpad: ", numpad)
print("Controller: ", controller)

# def paths_from_pair(source, dest, grid): #[str]
#     # print("Expanding: ", source, " to ", dest)

#     possible_sub_paths = []

#     # routes = 
#     for route in routes:
#         s = ""
#         for s, d in pairwise(route):
#             # print(grid[route[idx]][route[idx+1]]['command'], end="")
#             s += grid[s][d]['command']
#         s += "A"
#         possible_sub_paths.append(s)
#         # print("")
#     # print(source, ":", dest, " - ", possible_sub_paths)
#     return possible_sub_paths
@cache
def path_length(path, count):
    # print("finding length of ", path, " at ", count)
    if count == 26:
        # print("Hit bottom with: ", path)
        return len(path)
    if count == 0:
        grid = numpad
    else:
        grid = controller

    total = 0
    for source, dest in pairwise("A" + path):
        costs = []
        routes = nx.all_shortest_paths(grid, source, dest)
        for route in routes:
            s = ""
            for s1,d1 in pairwise(route):
                s+= grid[s1][d1]['command']
            s += 'A'

        # paths_from_pair(pair[0], pair[1], grid)
            # print(s)
            costs.append(path_length(s, count+1))
        # for next_path in next_paths:
        #     arr.append(path_length(next_path, count+1))
        # # print(next_paths)
        # print(arr)  
        total += min(costs)


    # print(path, " total returned is: ", total)
    return total
    
    # for idx in range(0, len(path) - 1):
    #     sub_paths = []
    #     arr = paths_from_pair(path[idx], path[idx+1], grid)
    #     sub_paths.append(arr)

    # path_total = 0
    # for sub_path in sub_paths:
    #     lengths = []
    #     for sub in sub_path:
    #         lengths.append(path_length(sub, count+1))
    #     print(lengths)
    #     path_total += min(lengths)
        
          
    #     # for sub_path in arr:
    #         # sub_path_costs.append(path_length(sub_path, count+1))
    #     # path_total += min(sub_path_costs)


    # return path_total

total = 0
for line in codes:
# line = codes[0]
# total = path_length("A" + line, 0)
    num_part = int(line[0:3])
    res = path_length(line, 0)
    total += num_part * res



# res = []
# for i in range(0, len(line) - 1):
#     res.append(paths_from_pair(line[i], line[i+1], numpad))
#     rt = []
#     for r in res:
#         pass

    print(res)
print("Part 1 totaL: ", total)

# def sub_path(path,print("A" + line)
# count):
#     pass

# def expand(commands):
    # arr = []
    # tot = 0
    # # print(pair_expand(commands[0], commands[1], 0))
    # # tot += pair_expand(commands[0], commands[1], 0)
    # for i in range(0, len(commands) - 1):
    #     tot += pair_expand(commands[i], commands[i+1], 0)
    # return tot
    # # if first_time:
    # first = nx.shortest_path(grid, "A", commands[0])
    # print("Moving from: ", first[0], "to ", commands[0])
    # for i in range(0, len(first) -1):
    #     print(grid[first[i]][first[i+1]]['command'], end="")
    #     s += grid[first[i]][first[i+1]]['command']
    # s += "A"
    # print("A")

    # for i in range(0, len(commands) - 1):
    #     s = ""
    #     routes = nx.all_shortest_paths(grid, commands[i], commands[i+1])
    #     print("Moving from: ", commands[i], " to ", commands[i+1], " with ", len(routes), " options")
    #     for route in routes:
    #         pass
    #     if len(enter) > 0:
    #         for idx in range(0, len(enter) - 1):
    #             print(grid[enter[idx]][enter[idx+1]]['command'], end="")
    #             s += grid[enter[idx]][enter[idx+1]]['command']
    #     s += "A"
    #     print("A")
    # return s

# print(line)
# first = nx.shortest_path(numpad, "A", line[0])
# for idy in range(0, len(first) - 1):
#     s += numpad[first[idy]][first[idy+1]]['command']
# s += "A"

# for idx in range(0, len(line) - 1):
#     enter = nx.shortest_path(numpad, line[idx], line[idx+1])
#     for idy in range(0, len(enter) - 1):
#         s += numpad[enter[idy]][enter[idy+1]]['command']
#     s += "A"
# s = "A" + s
# total = expand("A" + line)
# print(s)
# print("Step 1: ", line, ": ", s)
# s2 = expand(s, controller)
# print("Step 2: ", line, ": ", s2)
# s3 = expand(s2, controller)
# print("Step 3: ", line, ": ", s3, " length: ", len(s3))
# total += len(s3) * num_part
# s4 = expand(s3, controller)
# print("Step 4: ", line, ": ", s4)


