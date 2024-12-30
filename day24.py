import string
import re
import copy
import functools
import itertools
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

# data = sample2

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
done = False

while not done:
    done = True
    for out_wire, tup in gates.items():
        print("out: ", out_wire)
        print("tuple: ", tup)
        if tup[0] in wires and tup[1] in wires:
            wires[out_wire] = tup[2](wires[tup[0]], wires[tup[1]])
        else:
            done = False
    
    
print("After wires: ", wires)

s = ""
print("Z Values:")
for key, value in sorted(wires.items()):
    z_val = ""
    if key.startswith("z"):
        print(key, ":", value)
        s = str(int(value)) + s


print(int(s, 2))
total = 0
print(total)

# sorted()

