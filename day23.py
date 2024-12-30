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

data = aocd.get_data(day=23, year=2024)

sample = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

# data = sample
connections = data.splitlines()

G = nx.Graph()

for line in connections:
    com1, com2 = line.strip().split("-")
    G.add_edge(com1, com2)

print(G)
total = 0

for node1, node2, node3 in itertools.combinations(G.nodes(), 3):
    if node1.startswith("t") or node2.startswith("t") or node3.startswith("t"):
        if node1 in G.neighbors(node2) and node2 in G.neighbors(node3) and node3 in G.neighbors(node1):
            # print("Found: ", node1, " ", node2, " ", node3)
            total += 1

# total = 0 
print("Part 1 totaL: ", total)

mwc = nx.max_weight_clique(G, weight=None)
for m in sorted(mwc[0]):
    print(m, ",", end="")

print("")

# sorted()

