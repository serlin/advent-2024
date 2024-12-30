import string
import re
import copy
import functools
import itertools
from itertools import pairwise
import aocd
import operator

data = aocd.get_data(day=24, year=2024)

sample = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

sample2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

# ANDER
sample3 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""

# data = sample3

initial_wires_data, gates_data = data.strip().split("\n\n")

wires = {} # wire, state
gates = {} # out_wire -> (in_wire, in_wire, function)

print(initial_wires_data)

for line in initial_wires_data.splitlines():
    print(line)
    wire_name, val = line.strip().split(": ")
    wires[wire_name] = bool(int(val))

for line in gates_data.splitlines():
    info = line.split(" ")
    function_str = info[1]
    function = ""
    match function_str:
        case "AND":
            function = operator.and_
        case "OR":
            function = operator.or_
        case "XOR":
            function = operator.xor
    gates[info[-1]] = (info[0], info[2], function)

print("Wires: ", wires)
print("Gates: ", gates)


def run_circuit(loc_gates, loc_wires): #returns int value of z wires
    done = False
    count = 0
    while not done and count < 25:
        done = True
        count += 1
        for out_wire, tup in loc_gates.items():
            # print("out: ", out_wire)
            # print("tuple: ", tup)
            if tup[0] in loc_wires and tup[1] in loc_wires:
                loc_wires[out_wire] = tup[2](loc_wires[tup[0]], loc_wires[tup[1]])
            else:
                done = False
    # print("After wires: ", wires)

    s = ""
    for key, value in sorted(loc_wires.items()):
        if key.startswith("z"):
            # print(key, ": ", value)
            s = str(int(value)) + s
    if len(s) > 0:
        return int(s, 2)
    else:
        return -1

xs = ""
ys = ""
for key, value in sorted(wires.items()):
    if key.startswith("x"):
        print("x", key)
        xs = str(int(value)) + xs
    elif key.startswith("y"):
        print("y", key)
        ys =  str(int(value)) + ys
print (xs, " - ", ys)
x_val = int(xs,2)
y_val = int(ys,2)
print (x_val, " - ", y_val)

# combinations = itertools.permutations(gates.keys(), 8)
combinations = itertools.combinations(gates.keys(), 8)
for combo in combinations:
    # print("Checking: ", combo)
    swapped_wires = wires.copy()
    swapped_gates = gates.copy()
    for i in range(0, len(combo)//2):
        swap1 = combo[i*2]
        swap2 = combo[i*2+1]
        hold = swapped_gates[swap1]
        swapped_gates[swap1] = swapped_gates[swap2]
        swapped_gates[swap2] = hold
    i = run_circuit(swapped_gates, swapped_wires)
    # print(x_val, "+", y_val, "=")
    # print(i)
    if x_val + y_val == i:
        print("Eureka! ", combo)
        break
