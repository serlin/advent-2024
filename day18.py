import string
import re
import copy
import functools
import itertools
from functools import cmp_to_key
import networkx as nx
from enum import Enum
import aocd
from time import sleep

data = aocd.get_data(day=18, year=2024)

sample = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

# data = sample

lines = data.splitlines()
max_x = 70
max_y = 70
num_bytes = 1024
start_loc = (0, 0)
end_loc = (max_x, max_y)



G = nx.grid_2d_graph(max_x + 1, max_y + 1)

print(G)

for i, line in enumerate(lines):
    if i >= num_bytes:
        break
    x, y = line.strip().split(",")
    tup = (int(x), int(y))
    print("removing: ", tup)
    G.remove_node(tup)

print(G)
a = nx.shortest_path_length(G, source=start_loc, target=end_loc)
print(a)
print(len(a))

# aocd.submit(total, part="b", day=18, year=2024)
